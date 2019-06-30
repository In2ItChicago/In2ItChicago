import { Injectable } from '@nestjs/common';
import { SearchBounds } from 'src/interfaces/searchBounds';
import { EventDAL } from 'src/DAL/eventDAL';
import { timestampToDate } from 'src/utilities';

@Injectable()
export class EventService {
    async getEvents(query: any) {
        // if (!context.params.query) {
        //     throw new GeneralError('Query not found');
        // }
        
        // if ((query.address && !query.miles) || (query.miles && !query.address)) {
        //     throw new BadRequest("address and miles must be used together");
        // }

        let searchBounds: SearchBounds | null = null;
        if (query.address) {
            searchBounds = await geoSearch(app, query.address, parseFloat(query.miles));
            delete query.address;
            delete query.miles;
            Object.assign(query, searchBounds);
        }  
        //context.params.query = Object.assign(query, searchFields);
        //context.params.query.searchBounds = searchBounds;

        const eventDAL = new EventDAL();
        const events = eventDAL.getEvents(query);

        if (events) {
            const mappedEvents = events.map(result => {
                Object.assign(result, {
                    start_date: result.start_time.toLocaleDateString(),
                    start_time: result.start_time.toLocaleTimeString(),
                    end_date: result.end_time.toLocaleDateString(),
                    end_time: result.end_time.toLocaleTimeString()
                });
                
                return mappedEvents;
            });
        }
        return null;
    }

    async createEvents(contextData: any) {
        const invalid = contextData.filter(data => !(
            data.organization && 
            data.event_time && 
            (data.event_time.start_timestamp || data.event_time.start_timestamp === 0) && 
            (data.event_time.end_timestamp || data.event_time.end_timestamp === 0)));
        // if (invalid.length > 0) {
        //     throw new BadRequest('Invalid events. organization, event_time.start_timestamp, and event_time.end_timestamp are required', invalid);
        // }

        for (let i = 0; i < contextData.length; i++) {
            Object.assign(contextData[i], {
                start_time: timestampToDate(contextData[i].event_time.start_timestamp),
                end_time: timestampToDate(contextData[i].event_time.end_timestamp)
            });
            delete contextData[i].event_time;
            delete contextData[i].address;
        }

        const organizations = _(contextData)
            .groupBy(d => d.organization)
            .map((value, key) => key)
            .value();

        await this.deleteEvents({
            query: {
                organization: organizations,
            },
        });

        const eventDAL = new EventDAL();
        eventDAL.createEvents(contextData);
    }

    async deleteEvents(query: any) {
        const eventDAL = new EventDAL();
        eventDAL.deleteEvents(query);
    }
}
