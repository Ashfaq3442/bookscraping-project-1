import scrapy
from urllib.parse import urljoin


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books=response.css('article.product_pod')

        for book in books:
            relative_url=book.css("h3 a::attr(href)").get()
            if "catalogue/" in relative_url:
                book_url="https://books.toscrape.com/"+relative_url
            else:
                book_url="https://books.toscrape.com/catalogue/"+relative_url
            yield response.follow(book_url, callback=self.parse_book_page)

        next_page=response.css("li.next a::attr(href)").get()

        if next_page is not None:
            if "catalogue" in next_page:
                next_page_url="https://books.toscrape.com/"+next_page
            else:
                next_page_url="https://books.toscrape.com/catalogue/"+next_page
            yield response.follow(next_page_url, callback=self.parse)

    def parse_book_page(self,response):
        book_detail=response.css(".page_inner")
        book_url=response.url

        yield {
            "book_url":book_url,
            "Book Title": response.css("div.product_main h1::text").get(),
            "price": response.css("article.product_page p::text").get(),
            "Book Type": response.css("li a::text").getall()[2],
            "Rating":response.css("article.product_page p.star-rating::attr(class)").re_first(r"star-rating (\w+)"),
            "UPC":response.css("table.table-striped td::text").get(),
            "Product Type":response.css("table.table-striped td::text").getall()[1],
            "Tax":response.css("table.table-striped td::text").getall()[4],
            "Book Available": response.css("table.table-striped td::text").getall()[5],
            "Number Of Reviews":response.css("table.table-striped td::text").getall()[6],
            "Description":response.css(".product_page p::text").getall()[10],
        }



# import scrapy
# from urllib.parse import urljoin

# class BookspiderSpider(scrapy.Spider):
#     name = "bookspider"
#     allowed_domains = ["books.toscrape.com"]
#     start_urls = ["https://books.toscrape.com/"]

#     def parse(self, response):
#         books = response.css('article.product_pod')

#         for book in books:
#             relative_url = book.css("h3 a::attr(href)").get()
#             if "catalogue/" in relative_url:
#                 book_url = "https://books.toscrape.com/" + relative_url
#             else:
#                 book_url = "https://books.toscrape.com/catalogue/" + relative_url

#             # Pass book_url to parse_book_page as a new request without meta
#             yield response.follow(book_url, callback=self.parse_book_page)

#         # Pagination
#         next_page = response.css("li.next a::attr(href)").get()
#         if next_page is not None:
#             if "catalogue" in next_page:
#                 next_page_url = "https://books.toscrape.com/" + next_page
#             else:
#                 next_page_url = "https://books.toscrape.com/catalogue/" + next_page
#             yield response.follow(next_page_url, callback=self.parse)

#     def parse_book_page(self, response):
#         # Recalculate book_url from response.url
#         book_url = response.url

#         # Extract book details
#         yield {
#             "Book URL": book_url,
#             "Book Title": response.css("div.product_main h1::text").get(),
#             "price": response.css("article.product_page p.price_color::text").get(),
#             "Book Type": response.css("li a::text").getall()[2],
#             "Rating": response.css("article.product_page p.star-rating::attr(class)").re_first(r"star-rating (\w+)"),
#             "UPC": response.css("table.table-striped td::text").get(),
#             "Product Type": response.css("table.table-striped td::text").getall()[1],
#             "Tax": response.css("table.table-striped td::text").getall()[4],
#             "Book Available": response.css("table.table-striped td::text").getall()[5],
#             "Number Of Reviews": response.css("table.table-striped td::text").getall()[6],
#             "Description": response.css(".product_page p::text").getall()[10],
#         }
