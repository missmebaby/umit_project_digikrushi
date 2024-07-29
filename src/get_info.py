import json
import requests
import os
from functools import cache
import pandas as pd
from dotenv import load_dotenv

load_dotenv(dotenv_path="/etc/secrets/.env")

URL = "https://loadqa.ndapapi.com/v1/openapi"


rename_dict = {
    "D6820_2": "Crop",
    "D6820_5": "Crop Season",
    "I6820_6": "Land area utilized for production (Ha (Hectare))",
    "I6820_7": "Crop production (t (Tonne))",
    "I6820_8": "Crop yield (t/ha (Tonnes per Hectares))",
}

state_code_dict = {
    "Andaman and Nicobar Islands": {"AlphaCode": "AN", "Code": "35"},
    "Andhra Pradesh": {"AlphaCode": "AP", "Code": "28"},
    "Andhra Pradesh (New)": {"AlphaCode": "AD", "Code": "37"},
    "Arunachal Pradesh": {"AlphaCode": "AR", "Code": "12"},
    "Assam": {"AlphaCode": "AS", "Code": "18"},
    "Bihar": {"AlphaCode": "BH", "Code": "10"},
    "Chandigarh": {"AlphaCode": "CH", "Code": "4"},
    "Chattisgarh": {"AlphaCode": "CT", "Code": "22"},
    "Dadra and Nagar Haveli": {"AlphaCode": "DN", "Code": "26"},
    "Daman and Diu": {"AlphaCode": "DD", "Code": "25"},
    "Delhi": {"AlphaCode": "DL", "Code": "7"},
    "Goa": {"AlphaCode": "GA", "Code": "30"},
    "Gujarat": {"AlphaCode": "GJ", "Code": "24"},
    "Haryana": {"AlphaCode": "HR", "Code": "6"},
    "Himachal Pradesh": {"AlphaCode": "HP", "Code": "2"},
    "Jammu and Kashmir": {"AlphaCode": "JK", "Code": "1"},
    "Jharkhand": {"AlphaCode": "JH", "Code": "20"},
    "Karnataka": {"AlphaCode": "KA", "Code": "29"},
    "Kerala": {"AlphaCode": "KL", "Code": "32"},
    "Lakshadweep Islands": {"AlphaCode": "LD", "Code": "31"},
    "Madhya Pradesh": {"AlphaCode": "MP", "Code": "23"},
    "Maharashtra": {"AlphaCode": "MH", "Code": "27"},
    "Manipur": {"AlphaCode": "MN", "Code": "14"},
    "Meghalaya": {"AlphaCode": "ME", "Code": "17"},
    "Mizoram": {"AlphaCode": "MI", "Code": "15"},
    "Nagaland": {"AlphaCode": "NL", "Code": "13"},
    "Odisha": {"AlphaCode": "OR", "Code": "21"},
    "Pondicherry": {"AlphaCode": "PY", "Code": "34"},
    "Punjab": {"AlphaCode": "PB", "Code": "3"},
    "Rajasthan": {"AlphaCode": "RJ", "Code": "8"},
    "Sikkim": {"AlphaCode": "SK", "Code": "11"},
    "Tamil Nadu": {"AlphaCode": "TN", "Code": "33"},
    "Telangana": {"AlphaCode": "TS", "Code": "36"},
    "Tripura": {"AlphaCode": "TR", "Code": "16"},
    "Uttar Pradesh": {"AlphaCode": "UP", "Code": "9"},
    "Uttarakhand": {"AlphaCode": "UT", "Code": "5"},
    "West Bengal": {"AlphaCode": "WB", "Code": "19"},
}
#{'StateCode': 1},{'StateCode': 2},{'StateCode': 3},{'StateCode': 4},{'StateCode': 5},{'StateCode': 6},{'StateCode': 7},{'StateCode': 8},{'StateCode': 9},{'StateCode': 10},{'StateCode': 11},{'StateCode': 12},{'StateCode': 13},{'StateCode': 14},{'StateCode': 15},{'StateCode': 16},{'StateCode': 17},{'StateCode': 18},{'StateCode': 19},{'StateCode': 20},{'StateCode': 21},{'StateCode': 22},{'StateCode': 23},{'StateCode': 24},{'StateCode': 27},{'StateCode': 28},{'StateCode': 29},{'StateCode': 30},{'StateCode': 32},{'StateCode': 33},{'StateCode': 34},{'StateCode': 35},{'StateCode': 36},{'StateCode': 37},{'StateCode': 38}&ind=I6820_6,I6820_7,I6820_8&dim=Country,StateName,StateCode,DistrictName,DistrictCode,Year,D6820_2,D6820_5&pageno=1
params_dict = {
   # "API_Key": os.getenv("API_KEY_NDPI"),
    "API_Key": "gAAAAABmppUwTRBndLdAmFoBPkOSOgxWSUWCMfsdhai6V7rkM3QLnxeyu6Ar2k3coNvPzNCNrRuevtXV6RB0I8TxZu4pyVi6SIP6uzqEGP9tHcldP49ceM2q8nmofktxitZeEkBozWRuWxa7De9ytBk1EDsLtWguliTCEZLUXyD7MOmx5jKPT5Xj5M8p9tqDBdbBgBOPzNvr",
    "dim": "Country,StateName,StateCode,DistrictName,DistrictCode,Year,D6820_2,D6820_5",
    "ind": "I6820_6,I6820_7,I6820_8",
    "pageno": 1,
    "StateCode": "{'StateCode': 1}",
}


def parse_values(di: dict):
    ndi = {}
    for k, v in di.items():
        if k in rename_dict:
            if type(v) is dict:
                ndi[rename_dict[k]] = f"{float(v['avg']):.2f}"
            else:
                ndi[rename_dict[k]] = v.strip() if type(v) is str else v
        elif k == "Year":
            ndi[k] = di[k].split(", ")[-1].strip()
        else:
            ndi[k] = v.strip() if type(v) is str else v
    return ndi


def rename(li: list[dict]):
    nli = []
    for di in li:
        ndi = parse_values(di)
        nli.append(ndi)
    return nli


@cache
def get_data(state: str, pages: int = 1):
    if state not in state_code_dict:
        return "Invalid Input"
    sc = state_code_dict[state]["Code"]
    sc_str = str({"StateCode": sc})
    master_li = list()
    for i in range(1, pages + 1):
        new_url = (
            URL
            + f"?API_Key={params_dict['API_Key']}&StateCode={sc_str}&ind={params_dict['ind']}&dim={params_dict['dim']}&pageno={i}"
        )
        resp = requests.get(new_url)
        if not resp.ok:
            return "Invalid URL"
        try:
            resp = resp.json()["Data"]
        except KeyError:
            return "Data Not Available"
        else:
            master_li.extend(rename(resp))

    return master_li


def to_json(state: str):
    data = get_data(state, 2)
    return json.dumps(data, allow_nan=True, indent=4)


def to_csv(state: str):
    df = pd.DataFrame(get_data(state, 2))
    return df.to_csv(float_format="%.5f", index=False, encoding="UTF-8")
