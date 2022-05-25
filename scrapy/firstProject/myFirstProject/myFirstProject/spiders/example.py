import scrapy
import json

class ExampleSpider(scrapy.Spider):
    name = 'pm25'
    allowed_domains = ['https://data.epa.gov.tw']
    start_urls = ['https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate desc&format=json']

    def parse(self, response):
        # print(response.text)
        data = json.loads(response.text)
        list_sites = data["records"]

        for obj in list_sites:
            if obj["county"] == "南投縣":
                print(obj["site"] + " PM 2.5 資料 : ")
                print(obj["datacreationdate"])
                print(obj["pm25"])
