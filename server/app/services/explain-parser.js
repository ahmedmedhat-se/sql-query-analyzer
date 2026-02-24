export function parseExplain(explainJson) {
    const queryBlock = explainJson.query_block;
    if (!queryBlock) return {};
    
    const rowsExamined = extractRows(queryBlock) || 0;
    const cost = queryBlock.cost_info?.query_cost || null;
    
    let indexUsed = null;
    let scanType = null;
    if (queryBlock.table) {
        const table = Array.isArray(queryBlock.table) ? queryBlock.table[0] : queryBlock.table;
        if (table.access_type) scanType = table.access_type;
        if (table.key) indexUsed = table.key;
    }
    
    return { rowsExamined, cost, indexUsed, scanType };
};

function extractRows(node) {
    let total = 0;
    if (node.rows) total += node.rows;
    if (node.table) {
        if (Array.isArray(node.table)) {
            for (const t of node.table) total += extractRows(t);
        } else {
            total += extractRows(node.table);
        }
    }
    if (node.attached_subqueries) {
        for (const subq of node.attached_subqueries) total += extractRows(subq);
    }
    return total;
};