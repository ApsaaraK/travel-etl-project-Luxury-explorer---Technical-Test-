import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
from etl.logger import get_logger

load_dotenv()
logger = get_logger("loader")

def get_engine():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    name = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    connection_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(connection_string)

def load(df):
    logger.info("Starting data load to PostgreSQL")

    engine = get_engine()

    df.to_sql(
        name="bookings",
        con=engine,
        if_exists="replace",
        index=False
    )

    logger.info(f"Successfully loaded {len(df)} records into bookings table")