import { metricsdb_config } from "../../config/database.js";

export async function saveQuery(sql){
    const stmt = "INSERT INTO queries (sql_text) VALUES (?)";
    const [result] = await metricsdb_config.query(stmt, [sql]);
    return result.insertId;
};