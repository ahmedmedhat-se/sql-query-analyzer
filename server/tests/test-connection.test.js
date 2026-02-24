import { metricsdb_config, testdb_config } from "../config/database.js";

async function databaseTestConnection(){
    console.log("Testing Database Connection.");
    try {
        const testConnection = await testdb_config.getConnection();
        console.log("Test Database Connected Successfully.");
        testConnection.release();

        const metricsConnection = await metricsdb_config.getConnection();
        console.log("Metrics Database Connected Successfully.");
        metricsConnection.release();

        process.exit(0);
    } catch (error){
        console.error(`Database Connection Failed: ${error.message}`);
        process.exit(1);
    }
}

databaseTestConnection();