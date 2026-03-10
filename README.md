# Associate Data Engineer Technical Examination - Travel ETL Pipeline

> ETL pipeline that processes **12,000+ travel booking records** through extraction, cleaning, validation, and loading, with AWS S3 cloud integration.Designed and implemented by **Tiruni Apsara Karunarathna** · [@ApsaaraK](https://github.com/ApsaaraK)

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![AWS S3](https://img.shields.io/badge/AWS_S3-FF9900?style=flat&logo=amazons3&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)

---

## What This Does

An end-to-end ETL pipeline built for **Luxury Explorers**, a travel booking business domain.
Raw booking data (with real-world messiness) is extracted, cleaned, validated, stored in the cloud, and loaded into a structured PostgreSQL database ready for analysis.

```
Raw CSV  →  Extract  →  Transform  →  Validate  →  S3 Upload  →  PostgreSQL
```

---

## Pipeline Architecture

```
┌────────────────────────────────────────────────────┐
│  📄  raw_bookings.csv                              │
│  12,360 records · dirty data · 9 columns           │
└───────────────────┬────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────┐
│  EXTRACT                        extractor.py       │
│  Read CSV → DataFrame                              │
│  Log columns, types, record count                  │
└───────────────────┬────────────────────────────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
┌──────────────────┐  ┌────────────────────────────────────────────┐
│  ☁️  S3 Upload   │  │  TRANSFORM                transformer.py  │
│  → bucket/raw/   │  │  Remove duplicates       (-304 rows)       │
└──────────────────┘  │  Standardize casing      (Title Case)      │
                      │  Fix date formats        (→ YYYY-MM-DD)    │
                      │  Fill nulls              (median / Unknown) │
                      └──────────────┬─────────────────────────────┘
                                     │
                                     ▼
┌────────────────────────────────────────────────────┐
│  VALIDATE                        validator.py      │
│                                                    │
│  ✓  price > 0                                      │
│  ✓  rating between 1.0, 5.0                       │
│  ✓  booking_date not null                          │
│                                                    │
│  Passed: 10,398          Rejected: 1,717           │
└──────────┬─────────────────────────┬───────────────┘
           │                         │
           │                         ▼
           │              ┌──────────────────────────┐
           │              │  logs/rejected_records.csv│
           │              │  Saved with reject reason │
           │              └──────────────────────────┘
           │
           ▼
┌────────────────────────────────────────────────────┐
│  ☁️  S3 Upload                    s3_handler.py    │
│  cleaned_bookings_TIMESTAMP.csv                    │
│  → bucket/cleaned/                                 │
└───────────────────┬────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────┐
│  LOAD                              loader.py       │
│  SQLAlchemy + psycopg2                             │
│  → PostgreSQL · travel_etl · bookings table        │
│  10,398 records loaded                             │
└───────────────────┬────────────────────────────────┘
                    │
          ┌─────────┴──────────┐
          ▼                    ▼
┌──────────────────┐  ┌──────────────────────────────┐
│  🐘 PostgreSQL   │  │  ☁️  AWS S3                  │
│  travel_etl db   │  │  travel-etl-tiruni           │
│  10,398 records  │  │  eu-north-1                  │
│  4 indexes       │  │  raw/ + cleaned/             │
└──────────────────┘  └──────────────────────────────┘
```

---

## Project Structure

```
travel-etl-project/
├── run_pipeline.py          # Entry point, run this
├── .env.example             # Credential template
├── requirements.txt
│
├── data/
│   ├── generate_dataset.py  # Generates raw dirty dataset
│   └── raw_bookings.csv
│
├── etl/
│   ├── extractor.py         # Reads CSV into DataFrame
│   ├── transformer.py       # Cleans and standardizes data
│   ├── validator.py         # Applies business rules
│   ├── loader.py            # Loads to PostgreSQL
│   ├── s3_handler.py        # AWS S3 uploads
│   └── logger.py            # Timestamped logging
│
├── sql/
│   ├── schema.sql           # Table + indexes
│   └── queries.sql          # Analytical queries
│
└── logs/
    ├── pipeline_TIMESTAMP.log
    └── rejected_records.csv
```

---

## Setup

```bash
# 1. Clone
git clone https://github.com/ApsaaraK/travel-etl-project.git
cd travel-etl-project

# 2. Virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure credentials
copy .env.example .env

# 5. Create database schema
# Run sql/schema.sql in pgAdmin

# 6. Generate dataset
python data/generate_dataset.py

# 7. Run the pipeline
python run_pipeline.py
```

---

## Environment Variables

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=travel_etl
DB_USER=postgres
DB_PASSWORD=your_password

AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket
AWS_REGION=your_region
```

---

## Database Schema

```sql
CREATE TABLE bookings (
    id              SERIAL PRIMARY KEY,
    hotel_name      VARCHAR(100)  NOT NULL DEFAULT 'Unknown',
    category        VARCHAR(50)   NOT NULL DEFAULT 'Uncategorized',
    country         VARCHAR(50)   NOT NULL DEFAULT 'Unknown',
    price           NUMERIC(10,2) CHECK (price > 0),
    rating          NUMERIC(3,1)  CHECK (rating >= 1 AND rating <= 5),
    customer_name   VARCHAR(100),
    booking_date    DATE,
    payment_method  VARCHAR(50)
);

-- Performance indexes
CREATE INDEX idx_bookings_country   ON bookings(country);
CREATE INDEX idx_bookings_category  ON bookings(category);
CREATE INDEX idx_bookings_date      ON bookings(booking_date);
CREATE INDEX idx_bookings_price     ON bookings(price);
```

---

## Analytical Queries

**Top 10 categories by revenue**
```sql
SELECT category, COUNT(*) AS total_bookings,
       ROUND(SUM(price)::numeric, 2) AS total_revenue
FROM bookings
GROUP BY category ORDER BY total_revenue DESC LIMIT 10;
```

**Monthly booking growth**
```sql
SELECT DATE_TRUNC('month', booking_date) AS month,
       COUNT(*) AS total_bookings,
       ROUND(SUM(price)::numeric, 2) AS monthly_revenue
FROM bookings
WHERE booking_date IS NOT NULL
GROUP BY month ORDER BY month;
```

**Average rating by country**
```sql
SELECT country,
       ROUND(AVG(rating)::numeric, 2) AS avg_rating,
       ROUND(AVG(price)::numeric, 2)  AS avg_price
FROM bookings
GROUP BY country ORDER BY avg_rating DESC;
```

---

## Scalability Notes

| Concern | Current | At Scale |
|---------|---------|----------|
| Record volume | 12K, full load | 1M+, chunked with `chunksize=10000` |
| Scheduling | Manual `python run_pipeline.py` | Apache Airflow DAG |
| Partitioning | Single table | Partition by `booking_date` monthly |
| Failures | Logs per step | Dead-letter queue + retry logic |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Pipeline scripting |
| Pandas | Data transformation |
| PostgreSQL | Analytical data store |
| SQLAlchemy | Database ORM |
| AWS S3 + boto3 | Cloud file storage |
| python-dotenv | Secure credential loading |
| Faker | Realistic test data generation |

---

*Associate Data Engineer Technical Examination · Luxury Explorers · March 2026*