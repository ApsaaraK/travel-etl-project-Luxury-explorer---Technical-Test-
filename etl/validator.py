import pandas as pd
from etl.logger import get_logger

logger = get_logger("validator")

def validate(df):
    logger.info("Starting validation")
    
    rejected_reasons = []

    invalid_price = df[df["price"] <= 0].copy()
    invalid_price["rejection_reason"] = "Negative or zero price"
    rejected_reasons.append(invalid_price)

    invalid_rating = df[(df["rating"] < 1) | (df["rating"] > 5)].copy()
    invalid_rating["rejection_reason"] = "Rating out of range (1-5)"
    rejected_reasons.append(invalid_rating)

    invalid_date = df[df["booking_date"].isnull()].copy()
    invalid_date["rejection_reason"] = "Missing booking date"
    rejected_reasons.append(invalid_date)

    rejected_df = pd.concat(rejected_reasons).drop_duplicates()

    invalid_ids = rejected_df.index
    clean_df = df.drop(index=invalid_ids)

    if len(rejected_df) > 0:
        rejected_df.to_csv("logs/rejected_records.csv", index=False)
        logger.warning(f"Rejected {len(rejected_df)} records — saved to logs/rejected_records.csv")
    
    logger.info(f"Validation complete: {len(clean_df)} valid records remaining")
    return clean_df