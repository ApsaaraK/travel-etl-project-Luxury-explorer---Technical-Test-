import pandas as pd
from etl.logger import get_logger

logger = get_logger("extractor")

def extract(filepath):
    logger.info(f"Starting extraction from: {filepath}")
    
    df = pd.read_csv(filepath)
    
    logger.info(f"Extracted {len(df)} records with {len(df.columns)} columns")
    logger.info(f"Columns: {list(df.columns)}")
    
    return df