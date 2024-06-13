from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Configuration
from .schemas import ConfigurationCreate, ConfigurationUpdate

async def create_configuration(db: AsyncSession, configuration: ConfigurationCreate):
    db_configuration = Configuration(**configuration.dict())
    db.add(db_configuration)
    await db.commit()
    await db.refresh(db_configuration)
    return db_configuration

async def get_configuration(db: AsyncSession, country_code: str):
    result = await db.execute(select(Configuration).where(Configuration.country_code == country_code))
    return result.scalars().first()

async def update_configuration(db: AsyncSession, country_code: str, configuration: ConfigurationUpdate):
    db_configuration = await get_configuration(db, country_code)
    if db_configuration:
        for key, value in configuration.dict().items():
            setattr(db_configuration, key, value)
        await db.commit()
        await db.refresh(db_configuration)
        return db_configuration
    return None

async def delete_configuration(db: AsyncSession, country_code: str):
    db_configuration = await get_configuration(db, country_code)
    if db_configuration:
        await db.delete(db_configuration)
        await db.commit()
        return True
    return False
