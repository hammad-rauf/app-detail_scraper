from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import AppdetailItem

#from datetime import date

import mysql.connector

class AppdetailSpider(CrawlSpider):

    name = "appdetail"
    start_urls = [
                "https://apps.shopify.com/browse/all?app_integration_kit=off&app_integration_pos=off&pricing=all&requirements=off&sort_by=installed"
    ]

    categorys = ["all","store-design","sales-and-conversion-optimization","marketing","orders-and-shipping","customer-support","inventory-management",
                "reporting","productivity","finding-and-adding-products","finances","trust-and-security","places-to-sell"
    ]

    rules = (
        Rule(LinkExtractor(restrict_css=(["#CategoriesFilter .search-filter--is-selected .marketing-radio-label",".search-pagination.display--mobile.text-center .search-pagination__next-page-text"]))),
        Rule(LinkExtractor(restrict_css=(".grid.grid--bleed.grid--equal-height.search-results__grid")),callback="product"),  
    )

    #datee = date.today()

    privacy_policy = ["policy","privacy"]

    # detail = mysql.connector.connect(
    #     host = 'localhost',
    #     user = 'root',
    #     password = 'H@mmad123',
    #     database = 'appdetail'
    # )
    # detail_db = detail.cursor()
    # detail_db.execute("SELECT * FROM appdetail_table")
    # detail_result = detail_db.fetchall()

    # update = mysql.connector.connect(
    #     host = 'localhost',
    #     user = 'root',
    #     password = 'H@mmad123',
    #     database = 'update_detail'
    # )
    # update_db = update.cursor()
    # update_db.execute("drop table if exists update_table")
    # update_db.execute("CREATE TABLE update_table( date text, field_id text,title text, old_value text, new_value text)")

    #def __init__(self):
        
        #detail_db.execute("drop table if exists appdetail_table")
        #detail_db.execute("CREATE TABLE appdetail_table( app_link text, category text,title text, subtitle text, developer text, feature_1 text, feature_1_desc text, feature_2 text, feature_2_desc text, feature_3 text, feature_3_desc text, full_description text, images_links text, developper_website text, privacy_policy text, email text, pricing text)")

        

    def product(self, response):

        product = AppdetailItem()

        product["app_link"] = response.url
        product["app_link"] = product["app_link"].split("?")[0]

        category = response.css(".heading--5.ui-app-store-hero__kicker a::text").extract()
        seperate = "," 
        product["category"] = seperate.join(category)


        check = response.css(".block.app-listing__support-section.app-listing__section .app-support-list__item span::text").extract()

        product["privacy_policy"] = None

        for data in check:
            if "Privacy policy not provided" in data:
                product["privacy_policy"] = "Privacy policy not provided"


        if product["privacy_policy"] == None:
            for privacy in self.privacy_policy:
                product["privacy_policy"] = response.css(f"a[href*='{privacy}']::attr(href)").extract_first()

                if product["privacy_policy"] is not None:
                    break
    

        product["title"] = response.css(".heading--2.ui-app-store-hero__header__app-name::text").extract_first().replace("'","")
        product["subtitle"] = response.css(".heading--3.ui-app-store-hero__description::text").extract_first().replace("'","")

        product["developer"] = response.css(".heading-4.ui-app-store-hero__header__subscript  .body-link::text").extract_first()
        product["developper_website"] = response.xpath("//a[text()='Developer website']/@href").extract_first()

        check = response.css(".key-benefits-section").extract_first()

        if check != None:
            try:
                product["feature_1"] = response.css(".grid__item.grid__item--tablet-up-third.text-center.color-ink .block__heading.heading--3::text").extract()[0].replace("'","")
                product["feature_1_desc"] = response.css(".grid__item.grid__item--tablet-up-third.text-center.color-ink .block__content.text-major::text").extract()[0].replace("'","")
            except ValueError:
                product["feature_1"] = None
                product["feature_1_desc"] = None

            try:
                product["feature_2"] = response.css(".grid__item.grid__item--tablet-up-third.text-center.color-ink .block__heading.heading--3::text").extract()[1].replace("'","")
                product["feature_2_desc"] = response.css(".grid__item.grid__item--tablet-up-third.text-center.color-ink .block__content.text-major::text").extract()[1].replace("'","")
            except ValueError:
                product["feature_2"] = None
                product["feature_2_desc"] = None

            try:
                product["feature_3"] = response.css(".grid__item.grid__item--tablet-up-third.text-center.color-ink .block__heading.heading--3::text").extract()[2].replace("'","")
                product["feature_3_desc"] = response.css(".grid__item.grid__item--tablet-up-third.text-center.color-ink .block__content.text-major::text").extract()[2].replace("'","")
            except ValueError:
                product["feature_3"] = None
                product["feature_3_desc"] = None
        else:
            product["feature_1"] = None
            product["feature_1_desc"] = None
            product["feature_2"] = None
            product["feature_2_desc"] = None
            product["feature_3"] = None
            product["feature_3_desc"] = None         

        full_description = response.css(".ui-expandable-content__inner p::text").extract()

        for index,description in enumerate(full_description):
            full_description[index] = description.strip("\n <h4></h4>")

        seperate = "," 

        product["full_description"] = seperate.join(full_description)
        product["full_description"] = product["full_description"].replace("'","")

        images_link = response.css(".app-listing-media__thumbnail a::attr(href)").extract()
        seperate = ","
        product["images_links"] = seperate.join(images_link)

        email = response.css(".app-support-list__item span::text").extract()
        for data in email:
            if "@" in data and "." in data:
                product["email"] = data
                break

        pricing = []

        pricing_tag = response.css(".ui-card.ui-card--large-padding.pricing-plan-card")

        for pri in pricing_tag:

            title = pri.css(".pricing-plan-card__title-kicker::text").extract_first()

            if title != None:
                title = title.strip()

            desc = pri.css(".pricing-plan-card__title-sub-heading.pricing-plan-card__title-sub-heading--subdued::text").extract_first()
                
            price = pri.css(".pricing-plan-card__title-header::text").extract_first().strip()

            lis = pri.css(".bullet p::text").extract()

            seperate = "-"
            lis = seperate.join(lis)

            data = f"{title},{price},{desc},{lis}"

            data = data.strip()

            data = data.replace("\n","")

            data = data.replace("'","")

            pricing.append(data)

        seperate = "//"
        product["pricing"] = seperate.join(pricing)

        # flag = 0

        # for app in self.detail_result:

        #     if str(app[2]) == str(product["title"]):

        #         if str(product["app_link"]) != str(app[0]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','app_link','{product['title']}','{app[0]}'")
        #             flag = 1            

        #         if str(product["category"]) != str(app[1]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','category','{product['category']}','{app[1]}'")    
        #             flag = 1         

        #         if str(product["subtitle"]) != str(app[3]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','subtitle','{product['subtitle']}','{app[3]}'") 
        #             flag = 1 

        #         if str(product["developer"]) != str(app[4]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','developer','{product['developer']}','{app[4]}'") 
        #             flag = 1 

        #         if str(product["feature_1"]) != str(app[5]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_1','{product['feature_1']}','{app[5]}'") 
        #             flag = 1 

        #         if str(product["feature_1_desc"]) != str(app[6]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_1_desc','{product['feature_1_desc']}','{app[6]}'")
        #             flag = 1 

        #         if str(product["feature_2"]) != str(app[7]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_2','{product['feature_2']}','{app[7]}'")  
        #             flag = 1 

        #         if str(product["feature_2_desc"]) != str(app[8]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_2_desc','{product['feature_2_desc']}','{app[8]}'")  
        #             flag = 1 

        #         if str(product["feature_3"]) != str(app[9]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_3','{product['feature_3']}','{app[9]}'") 
        #             flag = 1 

        #         if str(product["feature_3_desc"]) != str(app[10]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_3_desc','{product['feature_3_desc']}','{app[10]}'") 
        #             flag = 1 

        #         if str(product["full_description"]) != str(app[11]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','full_description','{product['full_description']}','{app[11]}'") 
        #             flag = 1 

        #         if str(product["images_links"]) != str(app[12]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','images_links','{product['images_links']}','{app[12]}'") 
        #             flag = 1 

        #         if str(product["developper_website"]) != str(app[13]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','developper_website','{product['developper_website']}','{app[13]}'") 
        #             flag = 1 

        #         if str(product["privacy_policy"]) != str(app[14]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','privacy_policy','{product['privacy_policy']}','{app[14]}'") 
        #             flag = 1 

        #         if str(product["email"]) != str(app[15]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','email','{product['email']}','{app[15]}'") 
        #             flag = 1 

        #         if str(product["pricing"]) != str(app[16]):
        #             self.update_db.execute(f"insert into update_table values ('{self.datee}','pricing','{product['pricing']}','{app[16]}'") 
        #             flag = 1 
                    
        #         if flag:
        #             break

        yield product
