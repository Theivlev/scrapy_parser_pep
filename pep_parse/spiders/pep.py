import scrapy
from scrapy.utils.project import get_project_settings

from pep_parse.items import PepParseItem

settings = get_project_settings()


class PepSpider(scrapy.Spider):
    name = settings.get('NAME')
    allowed_domains = settings.get('ALLOWED_DOMAINS')
    start_urls = settings.get('START_URLS')

    def parse(self, response):
        sections = response.css('section#numerical-index')
        td_tag = sections.css('td')
        links = td_tag.css('a::attr(href)').getall()
        for link in links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = response.css('h1.page-title::text').get().split(' – ')
        number = number.split()[1]
        element = response.css('dl.rfc2822.field-list.simple')
        status = element.css('dt:contains("Status") + dd')
        status_text = status.css('abbr::text').get()
        data = {
            'number': number,
            'name': name,
            'status': status_text,
        }
        yield PepParseItem(data)
