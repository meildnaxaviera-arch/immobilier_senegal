import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import boto3

URL = "https://immobilier-au-senegal.com/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text

def parse_html(html: str) -> list:
    soup = BeautifulSoup(html, "html.parser")
    # Chaque bien immobilier semble être dans un <div> ou <article> avec un titre h3
    return soup.select("h3")  # on prendra le titre comme point d'entrée

def extract_properties(divs: list) -> list[dict]:
    properties = []
    for div in divs:
        title = div.text.strip()
        parent = div.parent
        location_tag = parent.find(text=lambda t: "Sénégal" in t)
        price_tag = parent.find(text=lambda t: "Fr" in t)
        added_tag = parent.find(text=lambda t: "Ajout" in t)
        
        properties.append({
            "title": title,
            "location": location_tag.strip() if location_tag else "",
            "price": price_tag.strip() if price_tag else "",
            "added": added_tag.strip() if added_tag else ""
        })
    return properties

def save_to_csv(properties: list[dict], filename: str):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title","location","price","added"])
        writer.writeheader()
        writer.writerows(properties)
    print(f"CSV généré : {filename}")


def upload_file_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_name)


# Exemple d'utilisation
file_path = "data/file.json"
file_name = "file.json"
MY_BUCKET_NAME = "m2dsia-mengue-meildna"


def main():
    html = fetch_html(URL)
    divs = parse_html(html)
    print(f"{len(divs)} biens trouvés")
    properties = extract_properties(divs)
    save_to_csv(properties, "immobilier_senegal.csv")
    upload_file_s3("immobilier_senegal.csv", MY_BUCKET_NAME, "immobilier_senegal.csv")

if __name__ == "__main__":
    main()
