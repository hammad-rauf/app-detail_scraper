# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import mysql.connector

from datetime import date


class AppdetailPipeline(object):

    def __init__(self):

        self.create_connection()
        self.datee = date.today()
        self.create_table()
        pass

    def create_connection(self):

        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = 'H@mmad123',
            database = 'appdetail'
        )
        self.curr = self.conn.cursor()

        detail_db = self.conn.cursor()
        detail_db.execute("SELECT * FROM appdetail_table")
        self.detail_result = detail_db.fetchall()

        update = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'H@mmad123',
        database = 'update_detail'
        )
        self.update_db = update.cursor()
    
    def create_table(self):

        self.curr.execute("drop table if exists appdetail_table")
        self.curr.execute("CREATE TABLE appdetail_table( app_link text, category text,title text, subtitle text, developer text, feature_1 text, feature_1_desc text, feature_2 text, feature_2_desc text, feature_3 text, feature_3_desc text, full_description text, images_links text, developper_website text, privacy_policy text, email text, pricing text)")
   
    def process_item(self, item, spider):

        for app in self.detail_result:

            if str(app[2]) == str(item["title"]):

                if str(item["app_link"]) != str(app[0]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','app_link','{item['title']}','{app[0]}'")            

                if str(item["category"]) != str(app[1]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','category','{item['category']}','{app[1]}'")             

                if str(item["subtitle"]) != str(app[3]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','subtitle','{item['subtitle']}','{app[3]}'")  

                if str(item["developer"]) != str(app[4]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','developer','{item['developer']}','{app[4]}'")  

                if str(item["feature_1"]) != str(app[5]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_1','{item['feature_1']}','{app[5]}'")  

                if str(item["feature_1_desc"]) != str(app[6]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_1_desc','{item['feature_1_desc']}','{app[6]}'") 

                if str(item["feature_2"]) != str(app[7]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_2','{item['feature_2']}','{app[7]}'")   

                if str(item["feature_2_desc"]) != str(app[8]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_2_desc','{item['feature_2_desc']}','{app[8]}'")   

                if str(item["feature_3"]) != str(app[9]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_3','{item['feature_3']}','{app[9]}'")  

                if str(item["feature_3_desc"]) != str(app[10]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','feature_3_desc','{item['feature_3_desc']}','{app[10]}'")  

                if str(item["full_description"]) != str(app[11]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','full_description','{item['full_description']}','{app[11]}'")  

                if str(item["images_links"]) != str(app[12]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','images_links','{item['images_links']}','{app[12]}'")  

                if str(item["developper_website"]) != str(app[13]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','developper_website','{item['developper_website']}','{app[13]}'")  

                if str(item["privacy_policy"]) != str(app[14]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','privacy_policy','{item['privacy_policy']}','{app[14]}'")  

                if str(item["email"]) != str(app[15]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','email','{item['email']}','{app[15]}'")  

                if str(item["pricing"]) != str(app[16]):
                    self.update_db.execute(f"insert into update_table values ('{self.datee}','pricing','{item['pricing']}','{app[16]}'")  
                    
                break

        self.store_db(item)

        return item

    def store_db(self,item):

        self.curr.execute(f"insert into appdetail_table values ('{item['app_link']}','{item['category']}','{item['title']}','{item['subtitle']}','{item['developer']}','{item['feature_1']}','{item['feature_1_desc']}','{item['feature_2']}','{item['feature_2_desc']}','{item['feature_3']}','{item['feature_3_desc']}','{item['full_description']}','{item['images_links']}','{item['developper_website']}','{item['privacy_policy']}','{item['email']}','{item['pricing']}')")
       
       
        self.conn.commit()


class DuplicatesPipeline(object):

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['title'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'])
            return item