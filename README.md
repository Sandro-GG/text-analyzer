# TextAnalyzer API

A FastAPI-based REST API for storing, analyzing, and managing text entries. It automatically calculates word counts, handles database pagination, and includes an isolated testing suite.

## Features
* **Text Analysis:** Automatically calculates word count upon submission.
* **CRUD Operations:** Complete endpoints to create, read, update, and delete text entries.
* **Pagination:** Query parameters (`limit` and `offset`) for efficient data retrieval.
* **Validation:** Rejects payloads exceeding 10,000 characters.
* **Robust Testing:** Full test suite running on an isolated, in-memory SQLite database.

## Tech Stack
* **Framework:** FastAPI
* **Database:** PostgreSQL (Development) / SQLite (Testing)
* **ORM:** SQLAlchemy 2.0
* **Testing:** Pytest, HTTPX (TestClient)

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/analyze` | Submit text for analysis and storage. |
| `GET` | `/history` | Retrieve history (supports `?limit=` and `?offset=`). |
| `PUT` | `/id/{id}` | Update an entry's text and recalculate the word count. |
| `DELETE` | `/id/{id}` | Delete a specific entry from the database. |