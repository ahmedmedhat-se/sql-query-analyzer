import { computeMetrics } from "../services/sql-metrics.js";
import { saveQuery } from "../repositories/query.js";
import { saveMetrics, getAllQueries, getQueryById } from "../repositories/metrics.js";

function hasSqlInjection(sql) {
    const dangerousPatterns = [
        /;\s*DROP\s+/i,
        /;\s*DELETE\s+/i,
        /;\s*UPDATE\s+/i,
        /;\s*INSERT\s+/i,
        /;\s*ALTER\s+/i,
        /;\s*CREATE\s+/i,
        /;\s*TRUNCATE\s+/i,
        /;\s*EXEC/i,
        /;\s*EXECUTE/i,
        /UNION\s+ALL\s+SELECT/i,
        /UNION\s+SELECT/i,
        /information_schema/i,
        /mysql\./i
    ];
    
    return dangerousPatterns.some(pattern => pattern.test(sql));
};

function isValidSqlQuery(sql) {
    if (!sql || typeof sql !== 'string') return false;
    
    const trimmed = sql.trim();
    if (trimmed.length === 0) return false;
    
    const validStart = /^\s*(SELECT|INSERT|UPDATE|DELETE|EXPLAIN|DESCRIBE|SHOW)\s+/i.test(trimmed);
    if (!validStart) return false;
    
    if (trimmed.length > 10000) return false;
    
    return true;
};

export async function submitQuery(req, res, next) {
    try {
        const { sql } = req.body;
        
        if (!sql) {
            return res.status(400).json({ error: 'SQL query is required' });
        }
        
        if (typeof sql !== 'string') {
            return res.status(400).json({ error: 'SQL query must be a string' });
        }
        
        if (hasSqlInjection(sql)) {
            return res.status(400).json({ error: 'Query contains potentially dangerous patterns' });
        }
        
        if (!isValidSqlQuery(sql)) {
            return res.status(400).json({ error: 'Invalid SQL query format' });
        }
        
        const trimmedSql = sql.trim();
        
        const metrics = await computeMetrics(trimmedSql);
        
        const queryId = await saveQuery(trimmedSql);
        await saveMetrics(queryId, metrics);
        
        res.status(201).json({
            message: 'Query analyzed and stored',
            queryId,
            metrics
        });
    } catch (error) {
        if (error.code === 'ER_PARSE_ERROR') {
            return res.status(400).json({ error: 'SQL syntax error' });
        }
        if (error.code === 'ER_NO_SUCH_TABLE') {
            return res.status(400).json({ error: 'Referenced table does not exist' });
        }
        if (error.message.includes('Query execution failed')) {
            return res.status(400).json({ error: error.message });
        }
        next(error);
    }
};

export async function getQueries(req, res, next) {
    try {
        const page = parseInt(req.query.page) || 1;
        const limit = parseInt(req.query.limit) || 50;
        
        if (page < 1 || limit < 1 || limit > 100) {
            return res.status(400).json({ error: 'Invalid pagination parameters' });
        }
        
        const queries = await getAllQueries(page, limit);
        res.json(queries);
    } catch (error) {
        next(error);
    }
};

export async function getQuery(req, res, next) {
    try {
        const { id } = req.params;
        
        const queryId = parseInt(id);
        if (isNaN(queryId) || queryId < 1) {
            return res.status(400).json({ error: 'Invalid query ID' });
        }
        
        const query = await getQueryById(queryId);
        if (!query) {
            return res.status(404).json({ error: 'Query not found' });
        }
        res.json(query);
    } catch (error) {
        next(error);
    }
};