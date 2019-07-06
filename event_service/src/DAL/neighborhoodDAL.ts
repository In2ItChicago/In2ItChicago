import * as knex from 'knex';
import * as _ from 'lodash';

const db = knex({
    client: 'postgresql',
    connection: 'postgresql://postgres:postgres@postgres:5432/events',
});

export class NeighborhoodDAL {
    async getNeighborhoods(): Promise<Array<Pick<any, 'neighborhood'>>> {
        const result = await db('geocode.location')
                    .distinct('neighborhood')
                    .whereNotNull('neighborhood')
                    .orderBy('neighborhood');

        return result;
    }
}