import { metricsdb_config } from "../../config/database.js";

export async function saveMetrics(query_id, metrics) {
    const {
        execution_time_ms, rows_examined, rows_returned, joins_count, index_used, complexity_score
    } = metrics;

    const stmt = `INSERT INTO query_metrics 
    (query_id, execution_time_ms, rows_examined, rows_returned, joins_count, index_used, complexity_score)
    VALUES (?, ?, ?, ?, ?, ?, ?)`;

    await metricsdb_config.query(stmt, [query_id, execution_time_ms, rows_examined, rows_returned, joins_count, index_used, complexity_score]);
};

export async function getAllQueries() {
    const stmt = 
    `SELECT q.id, q.sql_text, q.created_at, 
            qm.execution_time_ms, qm.rows_examined, qm.rows_returned,
            qm.joins_count, qm.index_used, qm.complexity_score
    FROM queries q
    LEFT JOIN query_metrics qm ON q.id = qm.query_id
    ORDER BY q.created_at DESC
    `;
    const [rows] = await metricsdb_config.query(stmt);
    return rows;
};

export async function getQueryById(id) {
    const stmt = 
    `SELECT q.id, q.sql_text, q.created_at, 
            qm.execution_time_ms, qm.rows_examined, qm.rows_returned,
            qm.joins_count, qm.index_used, qm.complexity_score
    FROM queries q
    LEFT JOIN query_metrics qm ON q.id = qm.query_id
    WHERE q.id = ?
    `;
    const [rows] = await metricsdb_config.query(stmt, [id]);
    return rows[0];
};