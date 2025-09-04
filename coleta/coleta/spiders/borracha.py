import scrapy


class BorrachaSpider(scrapy.Spider):
    name = "borracha"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/borracha-porta-geladeira?psafe_param=1"]

    def parse(self, response):

        products = response.css('div.ui-search-result__wrapper')

        for product in products:
            yield {
                'description': product.css('a.poly-component__title::text').get(),
                'currency': product.css('span.andes-money-amount__currency-symbol').get(),
                'price': product.css('span.andes-money-amount__fraction').get(),
                'cents': product.css('span.andes-money-amount__cents andes-money-amount__cents--superscript-24').get()
            }
        pass
