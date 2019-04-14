import * as _ from 'lodash';
import { GeneralError } from '@feathersjs/errors';
import { HookMap, Hook, HookContext } from '@feathersjs/feathers';

import { minExpireAfterDays, maxExpireAfterDays } from './settings';


export const sleep = (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs));

export function errorHandler(ctx: HookContext<any>): HookContext<any> {
    if (ctx.error) {
        const error = ctx.error;
        if (!error.code) {
            const newError = new GeneralError(`server error: ${error.stack}`);
            ctx.error = newError;
            return ctx;
        }
        
        console.log({
            message: ctx.error.message,
            stack: ctx.error.stack,
            data: ctx.error.data
        });
    }
    return ctx;
}

export const timestampToDate = (timestamp: number): Date => new Date(timestamp * 1000);

export const dateTimeFromTimestamp = (timestamp: number): Date => this.timestampToDate(timestamp).toISOString();

export const dateFromTimestamp = (timestamp: number): Date => this.timestampToDate(timestamp).toLocaleDateString();

export const timeFromTimestamp = (timestamp: number): Date => this.timestampToDate(timestamp).toLocaleTimeString();

export const getRandomInt = (min: number, max: number): number =>  Math.floor(Math.random() * (max - min)) + min;
    
export const daysToMilliseconds = (days: number): number => days * 24 * 60 * 60 * 1000;

export const addDaysToDate = (date: Date, days: number): Date => new Date(date.getTime() + this.daysToMilliseconds(days));

export function randomExpirationTime(): Date {
        let expirationTime = this.getRandomInt(minExpireAfterDays, maxExpireAfterDays);
        return this.addDaysToDate(new Date(), expirationTime);
    }
