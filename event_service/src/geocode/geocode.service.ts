import { Injectable, HttpService, Inject } from '@nestjs/common';
import { Observable } from 'rxjs';
import { AxiosResponse } from 'axios';
import { GeocodeDAL } from '@src/DAL/geocodeDAL';
import * as GeoPoint from 'geopoint';
import { readFileSync } from 'fs';
import * as GeoJsonGeometriesLookup from 'geojson-geometries-lookup';
import { AddressResult } from '@src/interfaces/addressResult';
import { sleep } from '@src/utilities';
import { GetGeocodeRequest } from '@src/DTO/getGeocodeRequest';
import { geocodeApiDelayMilliseconds } from '@src/settings';
import { GetGeocodeResponse } from '@src/DTO/getGeocodeResponse';
import { CoordPair } from '@src/interfaces/coordPair';
import { map } from 'lodash';
import { SearchNeighborhoodRequest } from '@src/DTO/searchNeighborhoodRequest';
import { plainToClass } from 'class-transformer';
import { EventDAL } from '@src/DAL/eventDAL';

const geojsonData = readFileSync('./res/chicago_neighborhoods.geojson');
const geojsonContent = JSON.parse(geojsonData.toString());
const geoLookup = new GeoJsonGeometriesLookup(geojsonContent);

/**
 * Service handling all requests for GeoCodes 
 */
@Injectable()
export class GeocodeService {
    lastExecuted: Date;

    constructor(
        private readonly httpService: HttpService, 
        @Inject('GeocodeDAL') private readonly geocodeDAL: GeocodeDAL,
        @Inject('EventDAL') private readonly eventDAL: EventDAL
    ) {
        this.lastExecuted = new Date();
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
        return plainToClass(GetGeocodeResponse, result);
    }

    async searchNeighborhood(query: SearchNeighborhoodRequest): Promise<GetGeocodeResponse[]> {
        const result = await this.geocodeDAL.searchNeighborhood(query);
        return plainToClass(GetGeocodeResponse, result);
    }

    async listNeighborhoods(): Promise<String[]> {
        const result = await this.geocodeDAL.getNeighborhoods();
        return result.map(r => r['neighborhood']);
    }

    async getGeocode(query: GetGeocodeRequest): Promise<GetGeocodeResponse> {
        const result = await this.geocodeDAL.getGeocode(query);

        if (result.length > 0) {
            return plainToClass(GetGeocodeResponse, result[0]);
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

    async clearAllGeocodes() {
        await this.eventDAL.nullifyGeocodeIds();
        await this.geocodeDAL.deleteAllGeocodes();
    }
}
