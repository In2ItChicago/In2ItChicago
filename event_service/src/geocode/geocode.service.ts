import { Injectable, HttpService, Inject } from '@nestjs/common';
import { Observable } from 'rxjs';
import { AxiosResponse } from 'axios';
import { SearchBounds } from '../interfaces/searchBounds';
import { GeocodeDAL } from '@src/DAL/geocodeDAL';
import * as GeoPoint from 'geopoint';
import { readFileSync } from 'fs';
import * as GeoJsonGeometriesLookup from 'geojson-geometries-lookup';
import { AddressResult } from 'src/interfaces/addressResult';
import { sleep } from '../utilities';
import { GetGeocodeRequest } from '@src/DTO/getGeocodeRequest';
import { geocodeApiDelayMilliseconds } from '../settings';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { CoordPair } from '@src/interfaces/coordPair';
import { map } from 'lodash';
import { SearchNeighborhoodRequest } from '@src/DTO/searchNeighborhoodRequest';

const geojsonData = readFileSync('./res/chicago_neighborhoods.geojson');
const geojsonContent = JSON.parse(geojsonData.toString());
const geoLookup = new GeoJsonGeometriesLookup(geojsonContent);

@Injectable()
export class GeocodeService {
    lastExecuted: Date;

    constructor(private readonly httpService: HttpService, @Inject('GeocodeDAL') private readonly geocodeDAL: GeocodeDAL) {
        this.lastExecuted = new Date();
    }
    async radiusSearch(request: GetGeocodeRequest, miles: number): Promise<SearchBounds> {
        let searchBounds: SearchBounds;
        const foundAddress = await this.geocodeDAL.getGeocode(request);
        if (foundAddress.lat && foundAddress.lon) {
            const point = new GeoPoint(parseFloat(foundAddress.lat), parseFloat(foundAddress.lon));
            const bounds = point.boundingCoordinates(miles);
            searchBounds = {
                minLat: Math.min(bounds[0]._degLat, bounds[1]._degLat),
                maxLat: Math.max(bounds[0]._degLat, bounds[1]._degLat),
                minLon: Math.min(bounds[0]._degLon, bounds[1]._degLon),
                maxLon: Math.max(bounds[0]._degLon, bounds[1]._degLon),
            };
        }
        return searchBounds;
    }

    async geoSearch(address: string): Promise<AddressResult | null> {
        const baseUrl = 'https://nominatim.openstreetmap.org/search';
        const diff = new Date().valueOf() - this.lastExecuted.valueOf();
        if (diff <= geocodeApiDelayMilliseconds) {
            await sleep(diff);
        }
        let response: AxiosResponse<CoordPair[]>;
        response = await this.httpService.get<CoordPair[]>(encodeURI(`${baseUrl}?q=${address}&format=json`)).toPromise();;

        this.lastExecuted = new Date();

        if (response.data.length === 0) {
            return {
                address,
                lat: null,
                lon: null,
                neighborhood: null,
            };
        }

        const data = response.data[0];
        const result: AddressResult = {
            address,
            lat: parseFloat(data.lat),
            lon: parseFloat(data.lon),
            neighborhood: null,
        };

        const geojsonPoint = { type: 'Point', coordinates: [data.lon, data.lat] };
        const matches = geoLookup.getContainers(geojsonPoint).features;
        if (matches.length > 0) {
            result.neighborhood = matches[0].properties.pri_neigh;
        }
        return result;
    }

    async getAllGeocodes(): Promise<GetGeocodeResponse[]> {
        const result = await this.geocodeDAL.getAllGeocodes();
        return result;
    }

    async searchNeighborhood(query: SearchNeighborhoodRequest): Promise<GetGeocodeResponse[]> {
        const result = await this.geocodeDAL.searchNeighborhood(query);
        return result;
    }

    async getGeocode(query: GetGeocodeRequest): Promise<GetGeocodeResponse> {
        // if (!query) {
        //     throw new GeneralError('Query not supplied');
        // }
        // searching by address and neighborhood causes issues if the neighborhood doesn't match the address
        // if (query.address && query.neighborhood) {
        //     delete query.neighborhood;
        // }

        const result = await this.geocodeDAL.getGeocode(query);

        // Geocode already found in database. No need to query web service.
        // if (result.length > 0) {
        //     if (query.address) {
        //         result = result[0];
        //     }
        //     return context;
        // }
        if (result.length > 0) {
            return result[0];
        }
        let webServiceResult: AddressResult | null = null;
        if (query.address) {
            webServiceResult = await this.geoSearch(query.address);
        }

        const id = await this.geocodeDAL.createGeocode(webServiceResult);
        return {
            id,
            address: webServiceResult.address,
            lat: webServiceResult.lat,
            lon: webServiceResult.lon,
            neighborhood: webServiceResult.neighborhood,
        };
    }
}
