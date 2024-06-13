from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, models, schemas, database

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await database.init_db()

@app.post("/create_configuration", response_model=schemas.Configuration)
async def create_configuration(configuration: schemas.ConfigurationCreate, db: AsyncSession = Depends(database.get_db)):
    return await crud.create_configuration(db, configuration)

@app.get("/get_configuration/{country_code}", response_model=schemas.Configuration)
async def get_configuration(country_code: str, db: AsyncSession = Depends(database.get_db)):
    db_configuration = await crud.get_configuration(db, country_code)
    if db_configuration is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_configuration

@app.post("/update_configuration", response_model=schemas.Configuration)
async def update_configuration(configuration: schemas.ConfigurationUpdate, db: AsyncSession = Depends(database.get_db)):
    db_configuration = await crud.update_configuration(db, configuration.country_code, configuration)
    if db_configuration is None:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return db_configuration

@app.delete("/delete_configuration/{country_code}")
async def delete_configuration(country_code: str, db: AsyncSession = Depends(database.get_db)):
    success = await crud.delete_configuration(db, country_code)
    if not success:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"detail": "Configuration deleted successfully"}
