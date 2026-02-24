import request from "supertest";
import app from "../app.js";

describe('POST /api/queries', () => {
    it('should analyze and store a valid SQL query', async () => {
        const res = await request(app)
                .post('/api/queries')
                .send({sql: 'SELECT * FROM employees LIMIT 1'});
        expect(res.statusCode).toBe(201);
        expect(res.body).toHaveProperty('queryId');
        expect(res.body.metrics).toHaveProperty('execution_time_ms');
    });

    it('should return 400 if no SQL provided', async () => {
        const res = await request(app).post('/api/queries').send({});
        expect(res.statusCode).toBe(400);
    });
});

describe('GET /api/queries', () => {
    it('should return list of queries', async () => {
        const res = await request(app).get('/api/queries');
        expect(res.statusCode).toBe(200);
        expect(Array.isArray(res.body)).toBe(true);
    });
});