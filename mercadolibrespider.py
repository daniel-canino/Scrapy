from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
 
class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()
 
 
class Mercadolibre(CrawlSpider):
    name = "Scrap-MercadoLibre"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 10
    }
 
    download_delay = 2
 
    allowed_domains = ["listado.mercadolibre.com.ve","articulo.mercadolibre.com.ve","mercadolibre.com.ve"]
 
    start_urls = ["https://listado.mercadolibre.com.ve/perros/"]
 
    rules = (
        # Paginacion
        Rule(
            LinkExtractor(
                allow=r'_Desde_'
            ),follow=True
        ),
        # Detalles de los productos
        Rule(
            LinkExtractor(
                allow=r'/MLV-'
            ), follow=True, callback='parse_items'
        ),
    )
 
    def Limpiartext(self, texto):
        nuevotext = texto.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').strip()
        return nuevotext
 
    def parse_items(self, response):
        sel = Selector(response)
        item = ItemLoader(Articulo(), sel)
        item.add_xpath('titulo', '//h1[@class="ui-pdp-title"]/text()',MapCompose(self.Limpiartext))
        item.add_xpath('precio', '/html/body/main/div/div[4]/div/div[1]/div/div[1]/div/div[2]/div/div[1]/div/span/span[3]/text()')
        item.add_xpath('descripcion', '//div[@class="ui-pdp-description"]/p/text()', MapCompose(self.Limpiartext))
 
        yield item.load_item()