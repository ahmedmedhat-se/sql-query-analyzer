import { analyzeSql } from "../utils/sql-analyzer.js";
import { parseExplain } from "./explain-parser.js";
import { executeAndAnalyze } from "./query-execution.js";

export async function computeMetrics(sql) {
    const { executionTimeMs, rowsReturned, explainJson } = await executeAndAnalyze(sql);
    const { rowsExamined, cost, indexUsed, scanType } = parseExplain(explainJson);
    const { joinsCount, hasSubquery, hasSelectStar, queryType } = analyzeSql(sql);
    
    let complexityScore = 0;
    if (joinsCount > 0) complexityScore += joinsCount;
    if (hasSubquery) complexityScore += 2;
    if (hasSelectStar) complexityScore += 1;
    if (queryType !== 'SELECT') complexityScore += 1;
    
    return {
        execution_time_ms: executionTimeMs,
        rows_examined: rowsExamined,
        rows_returned: rowsReturned,
        joins_count: joinsCount,
        index_used: indexUsed,
        scan_type: scanType,
        complexity_score: complexityScore,
        cost,
        has_subquery: hasSubquery,
        has_select_star: hasSelectStar,
        query_type: queryType
    };
};