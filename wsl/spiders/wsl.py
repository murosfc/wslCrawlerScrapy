import scrapy
import pandas as pd

class Athlete:
    def __init__(self):
        self.rank = ''
        self.name = ''
        self.total_points = ''
        self.heat_wins = ''
        self.avg_score = ''
        self.age = ''
    pass

class PapelSpider(scrapy.Spider):
    name = 'wsl'
    start_url = 'http://www.worldsurfleague.com/athletes/tour/mct?year=2022'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    def start_requests(self):
        yield scrapy.Request(self.start_url, headers=self.headers)

    def parse(self, response):
        athletes = response.xpath('//*[contains(@class,"tableType-athlete")]//tr')
        for athlete in athletes:
            object_athlete = Athlete()
            object_athlete.rank = athlete.css("td.athlete-rank::text").get()
            object_athlete.name = athlete.css("a.athlete-name::text").get()
            object_athlete.total_points = athlete.css("span.tour-points::text").get()
            url = athlete.css("a.athlete-name::href").get()
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_detail(object_athlete) )
            if object_athlete.rank is not None:
                yield {
                'rank': object_athlete.rank,
                'name': object_athlete.name ,
                'total points': object_athlete.total_points,
                'age': object_athlete.age,
                'average score': object_athlete.avg_score,
                'heat wins': object_athlete.heat_wins
                }

    def parse_detail(self, response, object_athlete):
        object_athlete.age = response.css("/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div/div[4]/ul/li[3]/div[2]/span[1]::text").get()
        object_athlete.avg_score = response.xpath("/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/ul/li[3]/div/div[2]::text").get()
        object_athlete.heat_wins = response.xpath('/html/body/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/div[2]/div/ul/li[2]/div/div[2]::text').get()




