from etl.extractor import extract
from etl.transformer import transform
from etl.validator import validate
from etl.loader import load
from etl.s3_handler import upload_to_s3
from etl.logger import get_logger
from datetime import datetime

logger = get_logger("pipeline")

def run():
    logger.info("..............PIPELINE STARTED ..............")

    # Extract
    df = extract("data/raw_bookings.csv")

    # Upload raw file to S3
    upload_to_s3("data/raw_bookings.csv", "raw/raw_bookings.csv")

    # Transform
    df = transform(df)

    # Validate
    df = validate(df)

    # Save cleaned data locally then upload to S3
    cleaned_path = "data/cleaned_bookings.csv"
    df.to_csv(cleaned_path, index=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    upload_to_s3(cleaned_path, f"cleaned/cleaned_bookings_{timestamp}.csv")

    # Load to PostgreSQL
    load(df)

    logger.info("..............PIPELINE COMPLETE ..............")

if __name__ == "__main__":
    run()