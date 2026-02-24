// App Imports
import express from "express";
import dotenv from "dotenv";
import morgan from "morgan";
import cors from "cors";

// API Routes Imports
import { queryRouter } from "./app/routes/query.routes.js";

dotenv.config();
const app = express();
const PORT = process.env.PORT || 3000;

// App Global Middlewares
app.use(express.json());
app.use(morgan(process.env.NODE_ENV === "production" ? "combined" : "dev"));
app.use(cors({
    origin: process.env.CORS_ORIGIN,
    credentials: process.env.CORS_CREDENTIALS === "true",
    optionsSuccessStatus: 200,
    exposedHeaders: ["RateLimit-Limit", "RateLimit-Remaining", "RateLimit-Reset"],
    methods: ["GET", "POST", "PUT", "DELETE", "PATCH"],
}));

// Web System APIs
app.use("/api/", queryRouter);

// Health Check Endpoint
app.get("/health", (req, res) => {
    res.status(200).json({
        success: true,
        message: "Server is running",
        timestamp: new Date().toISOString(),
        uptime: process.uptime()
    });
});

// 404 Handler
app.use((req, res) => {
    console.log(`404 endpoint is not found: ${req.method} ${req.originalUrl}.`);
    res.status(404).json({
        message: "Endpoint is not found.",
        success: false,
        path: req.originalUrl
    });
});

// Error Global Handler
app.use((err, req, res, next) => {
    console.error(`
Error: ${err.message}
Stack: ${err.stack}
Path: ${req.path}
Method: ${req.method}
IP: ${req.ip}
`);

    if (err.name === "RateLimitError") {
        return res.status(429).json({
            message: "Too many requests, try again later.",
            success: false,
            retryAfter: Math.ceil(err.retryAfter / 1000) || 900
        });
    }

    res.status(err.status || 500).json({
        message: "Internal Server Error.",
        success: false,
        ...(process.env.NODE_ENV === 'development' && { error: err.message })
    });
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('Unhandled Rejection at:', promise, 'reason:', reason);
});

process.on('uncaughtException', (error) => {
    console.error('Uncaught Exception:', error);
    if (process.env.NODE_ENV !== 'production') {
        process.exit(1);
    }
});

// App Initialization
app.listen(PORT, () => {
    console.log(`Server listening at http://localhost:${PORT}`);
});

export default app;

if (typeof module !== 'undefined' && module.exports) {
    module.exports = app;
};