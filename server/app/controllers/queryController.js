import { computeMetrics } from "../services/sql-metrics.js";
import { saveQuery } from "../repositories/query.js";
import { saveMetrics, getAllQueries, getQueryById } from "../repositories/metrics.js";

export async function submitQuery(req, res, next) {
    try {
        const { sql } = req.body;
        if (!sql) {
            return res.status(400).json({ error: 'SQL query is required' });
        }
        const metrics = await computeMetrics(sql);
        
        const queryId = await saveQuery(sql);
        await saveMetrics(queryId, metrics);
        
        res.status(201).json({
            message: 'Query analyzed and stored',
            queryId,
            metrics
        });
    } catch (error) {
        next(error);
    }
};

export async function getQueries(req, res, next) {
    try {
        const queries = await getAllQueries();
        res.json(queries);
    } catch (error) {
        next(error);
    }
};

export async function getQuery(req, res, next) {
    try {
        const { id } = req.params;
        const query = await getQueryById(id);
        if (!query) {
            return res.status(404).json({ error: 'Query not found' });
        }
        res.json(query);
    } catch (error) {
        next(error);
    }
};