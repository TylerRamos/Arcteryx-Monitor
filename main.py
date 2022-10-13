import requests
from datetime import datetime

class Arcteryx:
    def __init__(self):
        self.url = "https://mcprod.arcteryx.com/graphql"
        self.session = requests.Session()
        
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://arcteryx.com",
            "referer": "https://arcteryx.com/",
            "sec-ch-ua": 
                '''"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"''',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '''"Windows"''',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "store": "arcteryx_en",
            "user-agent": 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "x-country-code": "us",
            "x-is-checkout": "false",
            "x-jwt": "",
        }
        
    def monitor(self, sku):
        
        payload = {
            "query": (
                "query gqlGetProductInventoryBySkus($productSkus:[String!]){\nproducts(filter:{sku:{in:$productSkus}},pageSize:500){\nitems{\nname\nsku\n...on ConfigurableProduct {\nvariants{\nproduct{\nsku\nquantity_available\n}\n}\n}\n}\n}\n}"
            ),
            "variables": {
                "productSkus": [
                    sku
                ]
            }
        }
        
        while True:          
            try:
                monitorResponse = self.session.post(self.url, json=payload, headers=self.headers)
                
                for item in monitorResponse.json()["data"]["products"]["items"][0]["variants"]:
                    
                    if item["product"]["quantity_available"] > 0:
                        print(
                            f'In stock [{item["product"]["sku"]}] [{item["product"]["quantity_available"]}] [{datetime.now().strftime("%H:%M:%S:%f")[0:-2]}]'
                        ) 
                        
                    else:
                        print(
                            f'Out of stock [{item["product"]["sku"]}] [{item["product"]["quantity_available"]}] [{datetime.now().strftime("%H:%M:%S:%f")[0:-2]}]'
                        )
                        
            except Exception as error:
                print(f"Error while monitoring [{error}]")
             
if __name__ == "__main__":   
    arcteryx = Arcteryx()
    arcteryx.monitor("X000005160") #https://arcteryx.com/us/en/
