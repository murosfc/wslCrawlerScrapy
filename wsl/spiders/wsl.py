import scrapy

class PapelSpider(scrapy.Spider):
    name = 'wsl'
    start_url = 'http://www.worldsurfleague.com/athletes/tour/mct?year=2022'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

    def start_requests(self):
        yield scrapy.Request(self.start_url, headers=self.headers)

    def parse(self, response):
        athletes = response.xpath('//*[contains(@class,"tableType-athlete")]//tr')
        for surfer in athletes:
            rank = surfer.css("td.athlete-rank::text").get()
            name = surfer.css("a.athlete-name::text").get()
            total_points = surfer.css("span.tour-points::text").get()
            if rank is not None:
                yield {
                'rank': rank,
                'name': name,
                'total points': total_points,
                }





