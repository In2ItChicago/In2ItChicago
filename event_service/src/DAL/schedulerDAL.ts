import * as _ from 'lodash';
import { getDb } from '@src/DAL/setup';

const DAYS_TO_KEEP = 14;

const db = getDb('scheduler');

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