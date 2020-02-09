import * as knex from 'knex';
import * as knexStringcase from 'knex-stringcase';
import * as _ from 'lodash';

const DAYS_TO_KEEP = 14;

const db = knex(knexStringcase({
    client: 'postgresql',
    connection: {
        host: process.env.HOST,
        user: 'postgres',
        password: 'postgres',
        database: 'scheduler'
    }
}));

export class SchedulerDAL {
    async cleanupScheduler() {
        await this.cleanupExecutions();
        await this.cleanupAuditLog();
    }

    async cleanupExecutions() {
        await db('scheduler.jobauditlog')
            .where('createdTime', '<', this.getMinDate())
            .del();
    }

    async cleanupAuditLog() {
        await db('scheduler.execution')
            .where('scheduledTime', '<', this.getMinDate())
            .del();
    }

    getMinDate() {
        let d = new Date();
        d.setDate(d.getDate() - DAYS_TO_KEEP);
        return d;
    }
}