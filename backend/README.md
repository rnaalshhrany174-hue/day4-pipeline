# Asset Maintenance API

## Overview
This is a CRUD API for managing maintenance records of assets using FastAPI and Pydantic.

## Setup
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install fastapi[all] pandas
   ```
3. Place your `maintenance_assets.csv` file in the `backend` directory.

## Running the API
Run the application using:
```bash
uvicorn main:app --reload
```

## API Endpoints
- `GET /assets`: List all assets with optional filters.
- `GET /assets/{asset_id}`: Get a single asset by ID.
- `POST /assets`: Create a new asset.
- `PUT /assets/{asset_id}`: Update an existing asset.
- `DELETE /assets/{asset_id}`: Delete an asset.

## Testing
Run tests using:
```bash
pytest -q
```