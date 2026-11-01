import os

import pandas as pd
from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import SetItemValues, Batch
from recombee_api_client.exceptions import APIException

# Configurare credentiale Recombee (la fel ca la Lab 02)
# Se citesc din variabile de mediu ca token-ul privat sa nu ajunga in repository:
#   $env:RECOMBEE_DB = "..."; $env:RECOMBEE_TOKEN = "..."; $env:RECOMBEE_REGION = "eu-west"
DB_NAME = os.environ.get('RECOMBEE_DB', 'numele_bazei_tale_de_date')
PRIVATE_TOKEN = os.environ.get('RECOMBEE_TOKEN', 'tokenul_tau_privat')
REGION = os.environ.get('RECOMBEE_REGION', 'eu-west')

client = RecombeeClient(DB_NAME, PRIVATE_TOKEN, region=Region[REGION.upper().replace('-', '_')])

# Acelasi dataset folosit la Lab 02 (Kaggle - 7k Books with Metadata)
PATH_DATASET = 'books.csv'

# Valorile lipsa din CSV (NaN) se trimit ca None (null in Recombee),
# altfel Recombee ar primi textul "nan" sau ar respinge request-ul
def text(value):
    return None if pd.isna(value) else str(value)

def integer(value):
    # pandas citeste coloanele intregi cu valori lipsa ca float (ex.: 247.0)
    return None if pd.isna(value) else int(value)

def real(value):
    return None if pd.isna(value) else float(value)

def send_items():
    """Functie care citeste dataset-ul si trimite item-urile in Recombee"""
    df = pd.read_csv(PATH_DATASET)
    print(f"Se trimit {len(df)} item-uri in Recombee...")

    requests = []

    for index, row in df.iterrows():
        # ID-ul unic al cartii devine itemId in Recombee
        item_id = str(row['isbn13'])

        # Maparea proprietatilor definite la Lab 02 cu valorile din randul curent
        properties = {
            "title": text(row['title']),
            "subtitle": text(row['subtitle']),
            "authors": text(row['authors']),
            "categories": text(row['categories']),
            "description": text(row['description']),
            "thumbnail": text(row['thumbnail']),
            "published_year": integer(row['published_year']),
            "average_rating": real(row['average_rating']),
            "num_pages": integer(row['num_pages']),
            "ratings_count": integer(row['ratings_count']),
        }

        # Adaugam request-ul de setare a valorilor pentru item
        # (SetItemValues creează automat item-ul dacă acesta nu există)
        requests.append(SetItemValues(item_id, properties, cascade_create=True))

        # Trimitem in loturi (batch) de cate 100 pentru eficienta
        if len(requests) == 100:
            client.send(Batch(requests))
            requests = []
            print("S-a trimis un lot de 100 item-uri...")

    # Trimitem si restul ramanase (daca numarul total nu e multiplu de 100)
    if requests:
        client.send(Batch(requests))
        print("S-a trimis ultimul lot de item-uri.")

    print("Toate item-urile au fost trimise cu succes!")

if __name__ == "__main__":
    send_items()
