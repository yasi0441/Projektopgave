import sqlite3
import sys
from pathlib import Path

# Gem databasen i samme mappe som scriptet
BASE_DIR = Path(__file__).resolve().parent
# Modify database name
DB_PATH = BASE_DIR / "CarsDB.db"

# Modify table field names and datatypes
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS Cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    year INTEGER CHECK(year >= 0),
    image text
);
"""

# Modify data for own use
SEED_ROWS = [
    (1, "Audi RS6 Avant",2023, ""),
    (2, "Audi R8",2020, ""),
    (3, "Audi TT Coupe 45 TFSI Quattro",2022, ""),
    (4, "Audi RS3 Sportback",2011, ""),
    (5, "Audi RS e-tron GT",2021, ""),
    (6, "Audi A7 Sportback 55 TFSI Quattro",2018, ""),
    (7, "Audi Q2",2021, ""),
    (8, "Audi A1",2010, ""),
    (9, "BMW M8 Competition Coupe", 2019, ""),
    (10, "BMW M5 (F90)", 2018, ""),
    (11, "BMW M4 Competition (G82)", 2021, ""),
    (12, "BMW X6 M", 2009, ""),
    (13, "BMW i4 M50", 2021, ""),
    (14, "BMW M3 Touring (G81)", 2021, ""),
    (15, "BMW i8", 2014, ""),
    (16, "BMW M5 (F10)", 2014, ""),
    (17, "BMW M4 (F82)", 2016, ""),
    (18, "BMW M3 (E92)", 2010, ""),
    (19, "BMW M3 e46", 2003, ""),
    (20, "BMW M2 Competition", 2016, ""),
    (21, "BMW M3 Evolution II", 1988, ""),
    (22, "Chevrolet Corvette Z06 (C8)", 2022, ""),
    (23, "Chevrolet Camaro Z28", 2014, ""),
    (24, "Chevrolet Corvette Z06 (C6)", 2006, ""),
    (25, "Chevrolet Corvette Stingray Coupe (C7)", 2015, ""),
    (26, "Dodge Challenger SRT8", 2014, ""),
    (27, "Dodge Charger SRT Hellcat", 2015, ""),
    (28, "Dodge SRT Viper GTS", 2014, ""),
    (29, "Dodge Charger R/T", 1969, ""),
    (30, "Ferrari LaFerrari", 2016, ""),
    (31, "Ferrari 488 GTB", 2016, ""),
    (32, "Ferrari Enzo", 2002, ""),
    (33, "Ferrari SF90", 2022, ""),
    (34, "Ford F-150 Raptor", 2017, ""),
    (35,"Ford Mustang GT", 2015, ""),
    (36, "Ford Mustang GT Dark Horse", 2024, ""),
    (37, "Ford GT", 2017, ""),
    (38, "Ford Fiesta ST", 2011, ""),
    (39, "Ford Fiesta ST-Line", 2018, ""),
    (40, "Ford Focus RS", 2016, ""),
    (41, "Ford Focus RS", 2002, ""),
    (42, "Honda Civic Type-R", 1997, ""),
    (43, "Honda Civic EJ1 Coupe", 1993, ""),
    (44, "Honda Civic", 2018, ""),
    (45, "Honda S2000 Ultimate Edition", 2009, ""),
    (46, "Honda Integra Type-R", 1998, ""),
    (47, "Honda CR-X", 1988, ""),
    (48, "Hyundai Accent", 2012, ""),
    (49, "Hyundai Elantra N", 2022, ""),
    (50, "Hyundai i20 N", 2021, ""),
    (51, "Koenigsegg Gemera", 2021, ""),
    (52, "Koenigsegg Jesko", 2020, ""),
    (53, "Lamborghini Countach LPI 800-4", 2022, ""),
    (54, "Lamborghini Huracan LP580-2", 2018, ""),
    (55, "Lamborghini Aventador S", 2017, ""),
    (56, "Lamborghini Countach 25th Anniversary", 1989, ""),
    (57, "Lamborghini Urus SE", 2025, ""),
    (58, "Lamborghini Temerario", 2025, ""),
    (59, "Lamborghini Revuelto", 2024, ""),
    (60, "Mazda RX-7", 1999, ""),
    (61, "Mazda MX5", 1989, ""),
    (62, "Mazda RX-8", 2012, ""),
    (63, "Mazda 3", 2016, ""),
    (64, "Mclaren P1", 2014, ""),
    (65, "Mclaren 600LT", 2019, ""),
    (66, "Mclaren 720s", 2018, ""),
    (67, "Mercedes-Benz 190E 2.5-16", 1988, ""),
    (68, "Mercedes-AMG C 63", 2017, ""),
    (69, "Mercedes-AMG A 45", 2016, ""),
    (70, "Mercedes-Maybach S 680", 2021, ""),
    (71, "Mercedes-Maybach GLS 600", 2021, ""),
    (72, "Mercedes-Benz EQE", 2022, ""),
    (73, "Mercedes-Benz G 63", 2022, ""),
    (74, "Mitsubishi Lancer Evolution IX", 2007, ""),
    (75, "Mitsubishi Lancer Evolution X", 2008, ""),
    (76, "Mitsubishi Eclipse GSX", 1999, ""),
    (77, "Nissan GT-R Premium (R35)", 2017, ""),
    (78, "Nissan Skyline GT-R V-Spec (R34)", 1999, ""),
    (79, "Nissan 350Z", 2008, ""),
    (80, "Nissan Silvia K's (S14)", 1998, ""),
    (81, "Nissan Z Prototype", 2022, ""),
    (82, "Nissan Silvia Spec-R Aero (S15)", 1999, ""),
    (83, "Nissan Skyline GT-R V-Spec (R32)", 1993, ""),
    (84, "Nissan 180SX Type X", 1996, ""),
    (85, "Pagani Zonda Cinque", 2009, ""),
    (86, "Porsche 911 GT3 RS", 2019, ""),
    (87, "Porsche 718 Cayman GTS", 2018, ""),
    (88, "Porsche Taycan Turbo S", 2022, ""),
    (89, "SSC Tuatara", 2020, ""),
    (90, "Subaru BRZ Premium", 2014, ""),
    (91, "Subaru Impreza WRX STI", 1998, ""),
    (92, "Toyota GR86", 2022, ""),
    (93, "Toyota AE86", 1987, ""),
    (94, "Toyota Supra MK4", 1994, ""),
    (95, "Toyota Supra MK5", 2022, ""),
    (96, "Toyota GR Yaris", 2022, ""),
    (97, "Toyota Chaser", 1998, ""),
    (98, "Toyota Rav4", 2023, ""),
    (99, "Toyota Celica", 2000, ""),
    (100, "Volkswagen Golf GTI", 2016, ""),
    (101, "Volkswagen Golf GTI", 2025, ""),
    (102, "Volkswagen Polo GTi", 2019, ""),
    (103, "Volkswagen Passat", 2020, ""),
    (104, "Volvo 242DL", 1975, ""),
    (105, "Volvo V90", 2018, ""),
    (106, "Volvo V40", 2017, ""),
    (107, "Volvo S90", 2016, ""),
]

# Modify function as described
def init_db(db_path: Path = DB_PATH, reset: bool = False):
    with sqlite3.connect(db_path) as conn:
        conn.execute("PRAGMA foreign_keys = ON;")
        if reset:
            conn.execute("DROP TABLE IF EXISTS Cars;") # Modify table name
        conn.executescript(SCHEMA_SQL)
        # Modify number and names of fields in INSERT query
        conn.executemany(
            "INSERT OR IGNORE INTO Cars (id, model, year, image) VALUES (?, ?, ?, ?);",
            SEED_ROWS,
        )
        conn.commit()

if __name__ == "__main__":
    reset_flag = "--reset" in sys.argv
    init_db(reset=reset_flag)
    print(f"Cars db oprettet: {DB_PATH} (reset={reset_flag})")