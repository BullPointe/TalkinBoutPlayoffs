from multiprocessing.sharedctypes import Value
from wsgiref import headers
from bs4 import BeautifulSoup
import pandas as pd
import re
import urllib.request

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
    def set_url(self,url: str):
        self.scrape_url = url
        print("URL Changed to:",self.scrape_url," Status:",self.status)
    def get_url(self) -> str:
        return self.scrape_url
    def get_status(self) -> int:
        return self.status
    def parse_url(self) -> None:
        self.source = urllib.request.urlopen(self.scrape_url).read()
        self.soup = BeautifulSoup(self.source,'html.parser')
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
    def parse_stats(self):
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
        
        

        print(stats_list)

    def get_html_table_attr(self):
        if self.status > 0:
            print("Rows:",len(self.rows))
        else:
            print("Please Parse Html")




class Player_Statistics:

    def __init__(self) -> None:
        self.tables = []
    
    def add_table(name,df):
        self.tables[name] = df
    



def main():
    sc1 = Scraper()
    # pc1 = Player_Statistics()
    sc1.set_url(
        "https://sports.yahoo.com/nfl/stats/weekly/?sortStatId=PASSING_YARDS&selectedTable=0&week={%22week%22:19,%22seasonPhase%22:%22POSTSEASON%22}"
        )

    sc1.parse_url()
    sc1.parse_html()
    # print()
    sc1.get_html_table_attr()
    
    sc1.parse_stats()



if __name__ == "__main__":
    main()




# source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()


