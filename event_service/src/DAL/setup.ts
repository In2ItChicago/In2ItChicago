import * as knex from 'knex';
import * as knexStringcase from 'knex-stringcase';
import { highlight } from 'cli-highlight';
import { performance } from 'perf_hooks';

const times = {};
export const getDb = (database: string): knex<any, unknown[]> => {
  const db = knex(
    knexStringcase({
      client: 'postgresql',
      connection: {
        host: process.env.HOST,
        user: 'postgres',
        password: 'postgres',
        database: database,
      },
    }),
  );

  if (process.env.PROFILE_QUERIES === '1') {
    db.client
      .on('query', (query) => {
        let sql = replaceBindings(query.sql, query.bindings);

        const uid = query.__knexQueryUid;
        times[uid] = { sql, startTime: performance.now() };
      })
      .on('query-response', (response, query) => {
        const endTime = performance.now();
        const uid = query.__knexQueryUid;
        const startQuery = times[uid];

        console.log(
          highlight(startQuery.sql, { language: 'sql', ignoreIllegals: true }),
        );
        console.log(
          `Time: ${(endTime - startQuery.startTime).toFixed(3)} ms\n`,
        );
        delete times[uid];
      });
  }

  return db;
};

const replaceBindings = (sql: string, bindings: Array<any>): string => {
  for (let binding of bindings) {
    // Format dates
    if (typeof binding?.toISOString === 'function') {
      binding = binding.toISOString();
    }

    if (typeof binding === 'string') {
      binding = `'${binding}'`;
    }

    sql = sql.replace('?', binding);
  }

  return sql;
};
