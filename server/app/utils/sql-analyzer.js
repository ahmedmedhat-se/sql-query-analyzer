export function analyzeSql(sql){
    const upperSql = sql.toUpperCase();

    const joinsMatches = upperSql.match(/\bJOIN\b/g);
    const joinsCount = joinsMatches ? joinsMatches.length : 0;

    const hasSubquery = /SELECT\s.*\(.*SELECT/.test(upperSql);
    const hasSelectStar = /\bSELECT\s*\*\s*FROM/.test(upperSql);

    let queryType = 'UNKNOWN';
    if (/^\s*SELECT/i.test(sql)) queryType = 'SELECT';
    else if (/^\s*INSERT/i.test(sql)) queryType = 'INSERT';
    else if (/^\s*UPDATE/i.test(sql)) queryType = 'UPDATE';
    else if (/^\s*DELETE/i.test(sql)) queryType = 'DELETE';

    return { joinsCount, hasSubquery, hasSelectStar, queryType };
};