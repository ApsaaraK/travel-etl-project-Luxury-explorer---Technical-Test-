import pandas as pd
import numpy as np
from etl.logger import get_logger

logger = get_logger("transformer")

def transform(df):
    original_count = len(df)
    logger.info(f"Starting transformation on {original_count} records")

    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    logger.info("Standardized column names")

    df = df.drop_duplicates()
    logger.info(f"Removed duplicates: {original_count - len(df)} rows dropped")

    for col in ["category", "country", "hotel_name", "payment_method"]:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()
    logger.info("Standardized text casing")

    df["booking_date"] = pd.to_datetime(df["booking_date"], dayfirst=True, errors="coerce")
    logger.info("Standardized booking_date to datetime")

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    logger.info("Cleaned numeric columns")

    df["hotel_name"] = df["hotel_name"].fillna("Unknown")
    df["category"] = df["category"].fillna("Uncategorized")
    df["country"] = df["country"].fillna("Unknown")
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    logger.info("Filled missing string values")

    df["price"] = df["price"].fillna(df["price"].median())
    df["rating"] = df["rating"].fillna(df["rating"].median())
    logger.info("Filled missing numeric values with median")

    logger.info(f"Transformation complete: {len(df)} clean records")
    return df