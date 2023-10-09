from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base
from databases import Database

Base = declarative_base()

class UrlData(Base):
    __tablename__ = "urls_data"

    starting_url = Column(String, primary_key=True)
    sublinks_found = Column(Integer, default=0)
    suspect_links_found = Column(Integer, default=0)
    is_suspect = Column(Boolean, default=False)

DATABASE_URL = "sqlite:///./test.db"
database = Database(DATABASE_URL)
engine = create_engine(DATABASE_URL)

def setup_db():
    Base.metadata.create_all(engine)

async def connect_to_db():
    await database.connect()

async def disconnect_from_db():
    await database.disconnect()

async def insert_new_url(starting_url: str):
    query = UrlData.__table__.insert().values(starting_url=starting_url)
    await database.execute(query)


async def get_all_url_data():
    query = UrlData.__table__.select()
    return await database.fetch_all(query)

async def reset_all_url_data():
    query = UrlData.__table__.delete()
    await database.execute(query)
