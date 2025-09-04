import scrapy


class BorrachaSpider(scrapy.Spider):
    name = "borracha"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/borracha-porta-geladeira?psafe_param=1"]
    page_count = 1
    max_page = 15


    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper')

        for product in products:
            yield {
                'description': product.css('a.poly-component__title::text').get(),
                'currency': product.css('span.andes-money-amount__currency-symbol::text').get(),
                'price': product.css('span.andes-money-amount__fraction::text').get(),
                'cents': product.css('span.andes-money-amount__cents.andes-money-amount__cents--superscript-24::text').get()
            }

        if self.page_count < self.max_page:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next.a::attr(href)').get()
            if next_page:
                self.page_count =+ 1
                yield scrapy.Request(url=next_page, callback=self.parse)
        pass
 