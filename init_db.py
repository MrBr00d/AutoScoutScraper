import requests
from bs4 import BeautifulSoup
# from datetime import datetime
from time import sleep
import pandas as pd

def request_website(page, cartype):
    url = f"https://www.autoscout24.nl/lst?atype=C&body={cartype}&cy=NL&damaged_listing=exclude&desc=0&page={page}&powertype=kw&search_id=22ayf9w7x4y&sort=standard&source=listpage_pagination&ustate=N%2CU"
    payload = {}
    headers = {'Accept': '*/*'}

    response = requests.request("GET", url, headers=headers, data=payload).text
    return response

def get_listings(cartype) -> pd.DataFrame:
    guid = []
    price = []
    make = []
    model = []
    mileage = []
    fuel_type = []
    age = []
    transmission = []

    for i in range(1,21):
        print(f"page {i}")
        response = request_website(i, cartype)
        soup = BeautifulSoup(response)
        res = soup.find_all("article")

        for i in range(len(res)):
            guid.append(res[i]["data-guid"])
            price.append(res[i]["data-price"])
            make.append(res[i]['data-make'])
            model.append(res[i]["data-model"])
            mileage.append(res[i]["data-mileage"])
            fuel_type.append(res[i]["data-fuel-type"])
            age.append(res[i]['data-first-registration'])
            transmission.append(res[i].find("span", {"data-testid": "VehicleDetails-transmission"}).getText())
        sleep(1)
    
    
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
    cars = {"Hatchback": 1,
            "Cabrio": 2,
            "Coupe": 3,
            "SUV": 4,
            "Stationwagen": 5,
            "Sedan": 6,
            "MPV": 12,
            "Bedrijfswagen":13}
    for car, cartype in cars.items():
        data = get_listings(cartype)
        data.to_excel(f"{car}.xlsx")
    df = pd.read_excel("Hatchback.xlsx", index_col=0)
    df2 = pd.read_excel("SUV.xlsx", index_col=0)
    df3 = pd.read_excel("Coupe.xlsx", index_col=0)
    df4 = pd.read_excel("Cabrio.xlsx", index_col=0)
    df5 = pd.read_excel("Stationwagen.xlsx", index_col=0)
    df6 = pd.read_excel("Sedan.xlsx", index_col=0)
    df7 = pd.read_excel("MPV.xlsx", index_col=0)
    df8 = pd.read_excel("Bedrijfswagen.xlsx", index_col=0)
    pd.concat([df,df2,df3,df4,df5,df6,df7,df8]).to_excel("total.xlsx", index=False)