import requests
from bs4 import BeautifulSoup
# from datetime import datetime
from time import sleep
import pandas as pd
import tqdm
import random

def request_website(page, make):
    url = f"https://www.autoscout24.nl/lst/{make}?atype=C&cy=NL&damaged_listing=exclude&desc=0&page={page}&powertype=kw&search_id=pahs15wiz4&sort=standard&source=homepage_search-mask&ustate=N%2CU"
    payload = {}
    headers = {'Accept': '*/*'}

    response = requests.request("GET", url, headers=headers, data=payload).text
    return response

def get_listings(cartype) -> pd.DataFrame:
    print(f"Searching for {cartype}...\n")
    guid = []
    price = []
    make = []
    model = []
    mileage = []
    fuel_type = []
    age = []
    transmission = []

    for i in range(1,21):
        response = request_website(i, cartype)
        soup = BeautifulSoup(response)
        res = soup.find_all("article")

        for i in range(len(res)):
            pbar.update(1)
            guid.append(res[i]["data-guid"])
            price.append(res[i]["data-price"])
            make.append(res[i]['data-make'])
            model.append(res[i]["data-model"])
            mileage.append(res[i]["data-mileage"])
            fuel_type.append(res[i]["data-fuel-type"])
            age.append(res[i]['data-first-registration'])
            transmission.append(res[i].find("span", {"data-testid": "VehicleDetails-transmission"}).getText())
        sleep(1+random.random())
    
    
    df = pd.DataFrame({"guid": guid,
              "price": price,
              'make': make,
              'model': model,
              'mileage': mileage,
              "fuel_type": fuel_type,
              'age': age,
              'transmission': transmission})
    return df

if __name__ == "__main__":
    df = pd.DataFrame()
    cars = ["mercedes-benz", "audi", "bmw", "volkswagen", "Toyota", "Volvo", "ford", "mini", "peugeot", "citroen", "fiat", "hyundai", "kia", "nissan", "opel", "renault", "seat", "skoda"]
    pbar = tqdm.tqdm(total=int(len(cars)*20*20))
    for car in cars:
        data = get_listings(cartype=car)
        df = pd.concat([df,data])
    df.to_csv("output.csv", index=False)