import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()
random.seed(42)
np.random.seed(42)

NUM_RECORDS = 12000

COUNTRIES = ["Sri Lanka", "India","Vietnam","Singappore","Thailand","Malaysia","Japan","UAE","Bahrain","Australia"]
CATEGORIES = ["Adventure","Luxuary","Budget","Family","Business","Cultural","Wellness","Group Tour","Honey moon","Beach"]
HOTELS = ["Shangri-La","Hilton","Cinammon Grand","Taj Samudra","Jetwing Blue", "Amangalla","Cape weligama","The fotress","Anantara","Heritance Kandalama"]

rows = []

for i in range (NUM_RECORDS):
    row={
        "id":str(i+1),
        "hotel_name":random.choice(HOTELS),
        "category":random.choice(CATEGORIES),
        "country":random.choice(COUNTRIES),
        "price":round(random.uniform(50,2000),2),
        "rating":round(random.uniform(1,5),1),
        "customer_name":fake.name(),
        "booking_date":fake.date_between(start_date="-2y",end_date="today").strftime("%Y-%m-%d"),
        "payment-method":random.choice(["Credit Card", "Debit Card","Cash","Bank Transfer"])

    }
    rows.append(row)

df=pd.DataFrame(rows)

for col in ["hotel_name","category","country","price","rating"]:
    null_indices = df.sample(frac=0.05).index
    df.loc[null_indices, col] = np.nan

case_indices = df.sample(frac=0.1).index
df.loc[case_indices, "category"] = df.loc[case_indices, "category"].str.upper()
case_indices2 = df.sample(frac=0.1).index
df.loc[case_indices2,"country"]=df.loc[case_indices2, "country"].str.lower()

bad_rating = df.sample(frac=0.02).index
df.loc[bad_rating, "rating"] =round(random.uniform(6,10),1)

bad_price = df.sample(frac=0.02).index
df.loc[bad_price,"price"] = -abs(round(random.uniform(10,500),2))

duplicates = df.sample(frac=0.03)
df=pd.concat([df,duplicates],ignore_index=True)

mixed_date_indices = df.sample(frac=0.1).index
df.loc[mixed_date_indices,"booking_date"]=pd.to_datetime(
    df.loc[mixed_date_indices, "booking_date"]
).dt.strftime("%d/%m/%Y")

df.to_csv("data/raw_bookin.csv",index=False)
print(f"dataset generated :{len(df)}records saved to data/raw_booking.csv")

