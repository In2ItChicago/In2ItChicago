import { Injectable } from '@nestjs/common';
import { SearchBounds } from 'src/interfaces/searchBounds';
import { GeocodeDAL } from 'src/DAL/geocodeDAL';
import * as GeoPoint from 'geopoint';
import { readFileSync } from 'fs';
import * as GeoJsonGeometriesLookup from 'geojson-geometries-lookup';
import { AddressResult } from 'src/interfaces/addressResult';
import { sleep } from 'src/utilities';

const geojsonData = readFileSync('chicago_neighborhoods.geojson');
const geojsonContent = JSON.parse(geojsonData.toString());
const geoLookup = new GeoJsonGeometriesLookup(geojsonContent);

@Injectable()
export class GeocodeService {
    lastExecuted: Date;

    constructor() {
        this.lastExecuted = new Date();
    }
    async radiusSearch(address: string, miles: number): Promise<SearchBounds> {
        const geocodeDAL = new GeocodeDAL();
        let searchBounds: SearchBounds;
        const foundAddress = await geocodeDAL.getGeocode({query: {address: `${address} US`}});
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
        const diff = new Date().valueOf() - lastExecuted.valueOf();
        if (diff <= geocodeApiDelayMilliseconds) {
            await sleep(diff);
        }
        const response = await axios.get(encodeURI(`${baseUrl}?q=${address}&format=json`));
        this.lastExecuted = new Date();

        if (response.data.length === 0) {
            return null;
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

    async getGeocode(query: any) {
        // if (!query) {
        //     throw new GeneralError('Query not supplied');
        // }
        // searching by address and neighborhood causes issues if the neighborhood doesn't match the address
        if (query.address && query.neighborhood) {
            delete query.neighborhood;
        }

        const geocodeDAL = new GeocodeDAL();
        let result = geocodeDAL.getGeocode(query);

        // Geocode already found in database. No need to query web service.
        if (result.length > 0) {
            if (query.address) {
                result = result[0];
            }
            return context;
        }
        let webServiceResult: AddressResult | null = null;
        if (context.params.address) {
            webServiceResult = await getGeocode(context.params.address);
        }
        
        if (webServiceResult == null) {
            webServiceResult = {
                address: query.address,
                lat: null,
                lon: null,
                neighborhood: null
            }
        }

        const val = await geocodeDAL.createGeocode(result);
        context.result.id = val[0];
        return context;
    }
}
