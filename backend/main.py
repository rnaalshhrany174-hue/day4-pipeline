from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, constr, condecimal
from typing import List, Optional
import pandas as pd

app = FastAPI()

# Load data from CSV
assets_df = pd.read_csv('backend/maintenance_assets.csv')

class Asset(BaseModel):
    asset_id: constr(regex='^[A-Z0-9-]+$')
    name: str
    asset_type: str
    location: str
    criticality: constr(regex='^(Low|Medium|High|Critical)$')
    status: constr(regex='^(active|inactive|maintenance|inspection)$')
    last_inspection_date: str  # Ideally should be a date type
    operating_hours: condecimal(gt=0)
    notes: Optional[str] = None

@app.get('/assets', response_model=List[Asset])
async def list_assets(
    status: Optional[constr(regex='^(active|inactive|maintenance|inspection)$')] = None,
    criticality: Optional[constr(regex='^(Low|Medium|High|Critical)$')] = None,
    asset_type: Optional[str] = None,
    location: Optional[str] = None
):
    filtered_assets = assets_df
    if status:
        filtered_assets = filtered_assets[filtered_assets['status'] == status]
    if criticality:
        filtered_assets = filtered_assets[filtered_assets['criticality'] == criticality]
    if asset_type:
        filtered_assets = filtered_assets[filtered_assets['asset_type'] == asset_type]
    if location:
        filtered_assets = filtered_assets[filtered_assets['location'] == location]
    return filtered_assets.to_dict(orient='records')

@app.get('/assets/{asset_id}', response_model=Asset)
async def get_asset(asset_id: str):
    asset = assets_df[assets_df['asset_id'] == asset_id]
    if asset.empty:
        raise HTTPException(status_code=404, detail='Asset not found')
    return asset.iloc[0].to_dict()

@app.post('/assets', response_model=Asset)
async def create_asset(asset: Asset):
    new_asset = asset.dict()
    assets_df.loc[len(assets_df)] = new_asset
    return new_asset

@app.put('/assets/{asset_id}', response_model=Asset)
async def update_asset(asset_id: str, asset: Asset):
    index = assets_df[assets_df['asset_id'] == asset_id].index
    if index.empty:
        raise HTTPException(status_code=404, detail='Asset not found')
    assets_df.loc[index[0]] = asset.dict()
    return asset

@app.delete('/assets/{asset_id}')
async def delete_asset(asset_id: str):
    index = assets_df[assets_df['asset_id'] == asset_id].index
    if index.empty:
        raise HTTPException(status_code=404, detail='Asset not found')
    assets_df.drop(index, inplace=True)
    return {'detail': 'Asset deleted'}