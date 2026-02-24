import express from "express";
import { submitQuery, getQueries, getQuery } from "../controllers/queryController.js";

export const queryRouter = express.Router();

queryRouter.post('/queries', submitQuery);
queryRouter.get('/queries', getQueries);
queryRouter.get('/queries/:id', getQuery);