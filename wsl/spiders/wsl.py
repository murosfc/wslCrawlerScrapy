import scrapy
from datetime import date
import pandas as pd

class PapelSpider(scrapy.Spider):
    name = 'wsl'
    start_url = 'http://www.worldsurfleague.com/athletes'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    def start_requests(self):
        current_tour_url = self.start_url +'/tour/mct?year=' + str(date.today().year)
        yield scrapy.Request(current_tour_url, headers=self.headers)

    def parse(self, response):
        ranking = {}
        athletes = response.xpath('//*[contains(@class,"tableType-athlete")]//tr')
        for i, surfer in enumerate(athletes):
            if i > 0:
                ranking['rank'] = surfer.css("td.athlete-rank::text").get()
                print("\nRANK: ", ranking['rank'])
                ranking['name'] = surfer.css("a.athlete-name::text").get()
                ranking['country'] = surfer.css("span.athlete-country-name::text").get()
                ranking['total_points'] = surfer.css("span.tour-points::text").get()
                rounds = surfer.css("span.tooltip-item::text").getall()
                if ranking['rank'] is not None:
                    for j, round in enumerate(rounds):
                        key = 'round ' + str(j+1)
                        ranking[key] = round
                    yield ranking
        try:
            df = pd.read_csv("wsl.csv")
            df.to_excel("wslRank.xlsx")
        except:
            pass

