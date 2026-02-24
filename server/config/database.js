import mysql from "mysql2/promise.js";
import dotenv from "dotenv";
dotenv.config();

export const testdb_config = mysql.createPool({
    host: process.env.TEST_DB_HOST,
    user: process.env.TEST_DB_USER,
    password: process.env.TEST_DB_PASSWORD,
    database: process.env.TEST_DB_NAME,
    port: process.env.TEST_DB_PORT,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

export const metricsdb_config = mysql.createPool({
    host: process.env.METRICS_DB_HOST,
    user: process.env.METRICS_DB_USER,
    password: process.env.METRICS_DB_PASSWORD,
    database: process.env.METRICS_DB_NAME,
    port: process.env.METRICS_DB_PORT,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});