from extractor import extractor
from scraper import scraper
from datetime import datetime
import mysql.connector
import pytz

# Lists to hold extracted data
address = []
bed = []
bath = []
sqft = []
price = []
url_list = []
geo = []
final = [('Address', 'Bedrooms', 'Bathrooms', 'SqftArea', 'Geo', 'Price', 'Url', 'parcel_id', 'year_built', "ScrapedAt")]
runs = []
page = 1
run = True
year_built = []
parcel_id = []

# Scrape and extract data
while run:
    url = f"https://www.redfin.com/city/14441/WA/Port-Orchard/filter/sort=lo-distance,property-type=house+condo,max-price=600k,min-beds=4,min-baths=2,min-year-built=2024,viewport=47.52981411308594:47.426817286914066:-122.62171594921875:-122.75904505078125,no-outline,geo-address=Port+Orchard%0C+WA/page-{page}"
    scraper(url)
    trial = extractor(address, bed, bath, sqft, price, url_list, geo, final, parcel_id, year_built)
    runs.append(len(url_list))
    if page > 2 and runs[-1] == runs[-2]:
        run = False
    elif page > 10:
        run = False
    page += 1

# Get current PST datetime



# MySQL Database Configuration
db_config = {
    "host": "localhost",
    "user": "root",          # Replace with your MySQL username
    "password": "Nannu2005@",  # Replace with your MySQL password
    "database": "zillow_db"  # Replace with your database name
}

# Save Data to MySQL
try:
    # Connect to MySQL
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # Create table with a UNIQUE constraint on the Url field
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sale (
            id INT AUTO_INCREMENT PRIMARY KEY,
            Address VARCHAR(255),
            Bedrooms VARCHAR(10),
            Bathrooms VARCHAR(10),
            SqftArea VARCHAR(50),
            Geo VARCHAR(100),
            Price VARCHAR(50),
            Url VARCHAR(255) UNIQUE,
            ScrapedAt DATETIME,
            parcel_id VARCHAR(255),
            year_built VARCHAR(255)
        )
    """)

    # Insert data into the table, skipping duplicates
    insert_query = """
        INSERT INTO sale
        (Address, Bedrooms, Bathrooms, SqftArea, Geo, Price, Url, parcel_id, year_built, ScrapedAt)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        Address=VALUES(Address),
        Bedrooms=VALUES(Bedrooms),
        Bathrooms=VALUES(Bathrooms),
        SqftArea=VALUES(SqftArea),
        Geo=VALUES(Geo),
        Price=VALUES(Price),
        parcel_id=VALUES(parcel_id),
        year_built=VALUES(year_built),
        ScrapedAt=VALUES(ScrapedAt)
    """
    for row in final[1:]:  # Skip header
        cursor.execute(insert_query, row)

    # Commit the transaction
    connection.commit()
    print("Data successfully saved into local MySQL database, avoiding duplicates.")

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
