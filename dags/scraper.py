import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import numpy as np

def request_website(page:int) -> requests.Response:
    url = f"https://www.autoscout24.nl/lst?atype=C&cy=NL&desc=0&page={page}&search_id=nhip3icgk3&sort=standard&source=listpage_pagination&ustate=N%2CU"
    payload = {}
    headers = {'Accept': '*/*'}

    response = requests.request("GET", url, headers=headers, data=payload).text
    return response

def get_listings() -> np.array:
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
        response = request_website(i)
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
    data = get_listings()
    data.to_excel("export.xlsx")
