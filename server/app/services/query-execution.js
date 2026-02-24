import { testdb_config } from "../../config/database.js";

export async function executeAndAnalyze(sql) {
    const connection = await testdb_config.getConnection();
    
    try {
        const start = Date.now();
        const [rows] = await connection.query(sql);
        const executionTimeMs = Date.now() - start;
        const rowsReturned = rows.length;
        
        const [explainRows] = await connection.query('EXPLAIN FORMAT=JSON ' + sql);
        const explainJson = explainRows[0]['EXPLAIN'];
    
        return {
            executionTimeMs,
            rowsReturned,
            explainJson: JSON.parse(explainJson)
        };
    } catch (error) {
        throw new Error(`Query execution failed: ${error.message}`);
    } finally {
        connection.release();
    }
};