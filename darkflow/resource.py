# #### imports ####
import requests, os, json

#### class defination ####
class DarkFlow():
    def __init__(self):
        try:
            headers = {
                'authority': 'api.portfolioinsider.com',
                'Content-type': 'application/json',
                'Accept': 'application/json',
                'cookie': os.environ['DARKFLOW_COOKIE'],
            }
            params = {}
            response = requests.get(os.environ['DARKFLOW_URL'], params=params, headers=headers)
            self.response_json = response.json()
        except Exception as e:
            print("Error while request : {} ".format(e))

    def getDarkflowList(self):
        try:
            dartflowList = self.response_json["trending_up"]

            filtered_data = []
            for item in dartflowList:
                filtered_item = {
                    key: item[key] for key in ["name", "ticker", "perf", "algo_price"] if key in item
                }
                # Access nested JSON object and extract day.open value
                if "day" in item and "open" in item["day"]:
                    filtered_item["day_open"] = item["day"]["open"]
                filtered_data.append(filtered_item)

            return filtered_data
        except Exception as e:
            print("Error while treading up : {} ".format(e))