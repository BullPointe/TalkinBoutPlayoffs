from multiprocessing.sharedctypes import Value
from wsgiref import headers
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import re
import urllib.request
import requests


def is_num_or_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

class Scraper:  
    def __init__(self) -> None:
        self.status = 0
        self.scrape_url = None
    def set_url(self,url: str,name: str):
        self.scrape_url = url
        self.name = name
        print("URL Changed to:",self.scrape_url," Status:",self.status)
    def get_url(self) -> str:
        return self.scrape_url
    def get_status(self) -> int:
        return self.status
    def parse_url(self) -> None:
        # driver = webdriver.Chrome()
        # driver.get(self.scrape_url)
        # html = driver.page_source
        self.source = urllib.request.urlopen(self.scrape_url)
        r = requests.get(self.scrape_url)
        print(r.text)
        self.soup = BeautifulSoup(self)
        # print(self.soup)
    def parse_html(self) -> None:
        self.rows=list()
        self.header = None

        html_table = self.soup.find("table",{"class":"table graph-table W(100%) Ta(start) Bdcl(c) Mb(56px) Ov(h)"})
        is_header = True
        for row in html_table.findAll("tr"):
            if is_header:
                self.header = row
                is_header = False
            else:
                self.rows.append(row)

        self.status = 1
    def parse_stats(self, data):
        headers_list = list()
        stats_list = list()
        for col in self.header.findAll("th"):
            headers_list.append(col["title"])
        
        for row in self.rows:
            ind_stats = list()
            for col in row.findAll("th"):
                ind_stats.append(col.text)
            for col in row.findAll("td"):
                if is_num_or_float(col.text):
                    ind_stats.append(float(col.text))
                else:
                    ind_stats.append(col.text)

            #Add row
            stats_list.append(ind_stats)
        
        # fill dataframe
        df_stats = pd.DataFrame(stats_list, columns=headers_list)
        data.add_table(self.name,df_stats)


    def get_html_table_attr(self):
        if self.status > 0:
            print("Rows:",len(self.rows))
        else:
            print("Please Parse Html")

    


class Player_Statistics:

    def __init__(self) -> None:
        self.tables = {}
        self.table_IDS = ['Passing','Rushing','Receiving','Kicking','Kickoffs','Punting','Returns','Defense']
    
    def add_table(self,name,df):
        self.tables[name] = df
    
    def get_all_tables(self,scraper,base_url):
        for i,name in enumerate(self.table_IDS):
            url = base_url[0] + str(i) + base_url[1]
            scraper.set_url(url, name)
            scraper.parse_url()
            # scraper.parse_html()
            # scraper.parse_stats(self)
            


def main():
    sc1 = Scraper()
    pc1 = Player_Statistics()
    base_url = ["https://sports.yahoo.com/nfl/stats/weekly/?sortStatId=PASSING_YARDS&selectedTable=","&week={%22week%22:19,%22seasonPhase%22:%22POSTSEASON%22}"]
    pc1.get_all_tables(sc1,base_url)

    print(pc1.tables['Defense'])



if __name__ == "__main__":
    main()




# source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()


