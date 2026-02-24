# SQL Query Performance Analyzer Backend

> Developed by **Ahmed Medhat**

---
## 📋 Project Overview

A developer tool that allows users to submit SQL queries, executes them on a MySQL test database, extracts performance metrics, stores them, and provides analytics insights via a REST API. Built with **Node.js, Express, and MySQL**.

**Developed by:** Ahmed Medhat - Marwan Essa
**Project Type:** Backend / API Server / Data Analysis
**License:** Proprietary – All rights reserved

---
### SQL QUERY ANALYZER

```js
database/
├── schema.sql
└── seed.sql
```

```js
server/
├── app/
│   ├── controllers/
│   │   └── queryController.js
│   ├── repositories/
│   │   ├── metrics.js
│   │   └── query.js
│   ├── routes/
│   │   └── query.routes.js
│   ├── services/
│   │   ├── explain-parser.js
│   │   ├── query-execution.js
│   │   └── sql-metrics.js
│   ├── utils/
│   │   └── sql-analyzer.js
├── config/
│   └── database.js
├── node_modules/
├── tests/
│   ├── api.test.js
│   └── test-connection.test.js
├── .env
├── .gitignore
├── app.js
├── jest.config.js
├── package-lock.json
└── package.json
```

---
## 🛠️ Technologies Used

### 🖥️ Backend Technologies
| Technology                                                                                                                | Purpose                           | Version |
| ------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ------- |
| ![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)                | JavaScript Runtime Environment    | 18.x+   |
| ![Express.js](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)            | Web Application Framework         | 4.x     |
| ![CORS](https://img.shields.io/badge/CORS-000000?style=for-the-badge&logo=cors&logoColor=white)                           | Cross-Origin Resource Sharing     | 2.x     |
| ![Morgan](https://img.shields.io/badge/Morgan-000000?style=for-the-badge&logo=morgan&logoColor=white)                     | HTTP Request Logger               | 1.x     |
| ![Nodemon](https://img.shields.io/badge/Nodemon-76D04B?style=for-the-badge&logo=nodemon&logoColor=white)                  | Development Server Auto-Restart   | 3.x     |
| ![Dotenv](https://img.shields.io/badge/Dotenv-000000?style=for-the-badge&logo=dotenv&logoColor=white)                     | Environment Variables Loader      | 16.x    |
| ![MySQL2](https://img.shields.io/badge/MySQL2-005C84?style=for-the-badge&logo=mysql&logoColor=white)                      | MySQL Database Driver             | 3.x     |

---
## Features
- Submit any SQL query (SELECT, INSERT, UPDATE, DELETE) via API.
- Automatically runs `EXPLAIN FORMAT=JSON` to capture query plan and times execution.
- Computes metrics: execution time, rows examined, rows returned, joins count, index usage, complexity score.
- Stores queries and metrics in a separate database for historical analysis.
- Provides endpoints to retrieve query history and details.
- Designed for collaboration with data analysts (export metrics for dashboards).

---
## 🚀 Getting Started
### Prerequisites
* **Node.js** v18 or higher
* **MySQL** v8 or higher
* **npm**

---
# 📖 API Documentation
### Base URL: *http://localhost:PORT/api*

### Query
* `POST /api/queries` – Submit and analyze a SQL query.
* `GET /api/queries` – Retrieve all analyzed queries with their metrics.
* `GET /api/queries/:id` – Retrieve a specific query by ID with its metrics.

---
## 📦 Available NPM Scripts
The project includes a set of utility scripts to simplify development, database migrations, and seeding.

## Setup & Installation
1. **Clone the repository**
```bash
   git clone https://github.com/ahmedmedhat-se/sql-query-analyzer.git
   cd sql-query-analyzer
```

2. **Install dependencies**
```bash
   npm install
```

3. **Configure environment variables**
```bash
   PORT=

   TEST_DB_HOST=
   TEST_DB_USER=
   TEST_DB_PASSWORD=
   TEST_DB_NAME=test_db
   TEST_DB_PORT=
   
   METRICS_DB_HOST=
   METRICS_DB_USER=
   METRICS_DB_PASSWORD=
   METRICS_DB_NAME=metrics_db
   METRICS_DB_PORT=
```

4. **Set up databases**
   · Ensure MySQL is running.
   · Run the schema script to create met

---
## 🤝 Contributing
This is a **proprietary project**. External contributions are **not accepted**.

---
## 📄 License
**PROPRIETARY LICENSE**
© 2026 - Ahmed Medhat, Marwan Essa. All Rights Reserved.
This project is a personal, non-commercial work created solely for the purpose of demonstrating full-stack web development skills.

## 👥 Author
* **Ahmed Medhat** – Junior Backend Engineer
* **Marwan Essa** – Data Analyst