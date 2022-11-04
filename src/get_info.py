import requests
import pandas as pd
import os


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

params_dict = {
    "API_Key": os.getenv('API_KEY_NDPI'),
    "dim": "Country,StateName,StateCode,DistrictName,DistrictCode,Year,D6820_2,D6820_5",
    "ind": "I6820_6,I6820_7,I6820_8",
    "pageno": 1,
    "StateCode": "{'StateCode': 1}",
}


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
            resp = resp.json()
            # df = pd.DataFrame(resp["Data"]).rename(rename_dict, axis=1)
            master_li.extend(resp["Data"])
        except KeyError:
            return "Data not Available"
    df = pd.DataFrame(master_li).rename(rename_dict, axis=1)
#     df.to_json(
#         f"../resources/downloads/json/data_{state.lower().strip().replace(' ', '_')}.json",
#         orient="records",
#         double_precision=5,
#         indent=4,
#     )
#     df.to_csv(
#         f"../resources/downloads/csv/data_{state.lower().strip().replace(' ', '_')}.csv",
#         float_format="%.5f",
#         index=False,
#     )
    return df.to_dict(orient="records")
