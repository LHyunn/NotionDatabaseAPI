import requests
import json
import datetime
from pprint import pprint

class NotionDatabase():
    def __init__(self, notion_database_id, notion_key):
        #init이 실행되면 notion_database_id의 데이터베이스에 있는 모든 페이지의 정보를 가져온다.
        #Notion에서 날짜의 형식은 2023-01-01T00:00:00.000+09:00 이다.
        self.notion_database_id = notion_database_id
        self.notion_key = notion_key
        self.database_url = "https://api.notion.com/v1/databases/" + self.notion_database_id + "/query"
        self.created_url = "https://api.notion.com/v1/pages"
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.notion_key,
            "Notion-Version": "2022-06-28",
            "content-type": "application/json"
        }
        self.property_dict = self.get_page_values()
        self.page_form = self.create_page_values_form()
        
    def transform_date(self, date):
        #str로 date를 받아서 datetime으로 변환한다.
        #datetime으로 변환한 후에 다시 str로 변환한다.
        #Notion에서 날짜의 형식은 2023-01-01T00:00:00.000+09:00 이다.
        date = datetime.datetime.strptime(date, "%Y%m%d%H%M%S").strftime("%Y-%m-%dT%H:%M:%S.000+09:00")
        return date
        
    def print_property_dict(self):
        pprint(self.property_dict)
        
    def print_page_form(self):
        pprint(self.page_form)
        
    def get_page_values(self):
        payload = { "page_size": 1 }
        response = requests.post(self.database_url, json=payload, headers=self.headers)
        properties = response.json()["results"][0]["properties"]
        property_keys = list(properties.keys())
        property_types = list(properties.values())
        for i in range(len(property_types)):
            property_types[i] = property_types[i]["type"]
        property_dict = {}
        for i in range(len(property_keys)):
            property_dict[property_keys[i]] = property_types[i]
        return property_dict
    
    def create_page_values_form(self):
        page_data = {
            "parent": {"database_id": self.notion_database_id},
            "properties": {}
        }
        for property_key, property_type in self.property_dict.items():
            if property_type == "select" or property_type == "status" or property_type == "number":
                page_data["properties"][property_key] = {
                    "type": property_type,
                    property_type: {
                        "name": ""
                    }
                }
            elif property_type == "date":
                page_data["properties"][property_key] = {
                    "type": property_type,
                    property_type: {
                        "start": "",
                        "end": None,
                        "time_zone": None
                    }
                }
            elif property_type == "rich_text" or property_type == "title":
                page_data["properties"][property_key] = {
                    "type": property_type,
                    property_type: [
                        {
                            "type": "text",
                            "text": {
                                "content": "",
                            }
                        }
                    ]
                }
        return page_data
    
    def upload_page_values(self, page_values):
        for property_key, property_value in page_values.items():
            if property_key == "formula" or property_key == "created_date":
                continue
            if property_key not in self.property_dict.keys():
                raise KeyError("property_key가 property_dict의 key에 없습니다.")
            if self.property_dict[property_key] == "select" or self.property_dict[property_key] == "status":
                self.page_form["properties"][property_key][self.property_dict[property_key]]["name"] = property_value
            elif self.property_dict[property_key] == "date":
                self.page_form["properties"][property_key][self.property_dict[property_key]]["start"] = property_value
            elif self.property_dict[property_key] == "rich_text" or self.property_dict[property_key] == "title":
                self.page_form["properties"][property_key][self.property_dict[property_key]][0]["text"]["content"] = property_value
            elif self.property_dict[property_key] == "number":
                self.page_form["properties"][property_key][self.property_dict[property_key]] = property_value
        data = json.dumps(self.page_form)
        res = requests.post(self.created_url, headers=self.headers, data=data)
        if res.status_code == 200:
            return True
        else:
            pprint(res.status_code)
            pprint(res.text)
