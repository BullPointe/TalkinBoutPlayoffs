from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import pandas as pd
from selenium.common.exceptions import NoSuchElementException        
import pickle
from connect_to_db import DatabaseConnection


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
    def create_driver(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
    def close_driver(self):
        self.driver.quit()
    def parse_url(self) -> None:
        # html = driver.page_source
        # self.source = urllib.request.urlopen(self.scrape_url)
        # r = requests.get(self.scrape_url)
        # print(r.text)
        self.driver.get(self.scrape_url)
        self.soup = BeautifulSoup(self.driver.page_source,"html.parser")
        
        # print(self.soup)a
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

        self.status += 1
    def parse_stats(self, data: 'PlayerStatistics', append=False):
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
                    if(col.text == '-'):
                        ind_stats.append(0.0)
                    else:
                        ind_stats.append(col.text)

            #Add row
            stats_list.append(ind_stats)
        
        # fill dataframe
        df_stats = pd.DataFrame(stats_list, columns=headers_list)

        if append == False:
            data.add_table(self.name,df_stats)
        else:
            data.tables[self.name] = pd.concat([data.tables[self.name], df_stats], ignore_index=True)

    def parse_all_stats(self,data):
        self.parse_stats(data,append=False)
            
        isMore = True
        try:
            # elements = scraper.driver.find_elements_by_class_name("D(ib) Mstart(8px)")
            elements = self.driver.find_elements_by_xpath("//li[@class='D(ib) Mstart(8px)']")
        except NoSuchElementException:
            print("Not Found")
            isMore = False

        if isMore:
            print("More")
            for idx in range(len(elements)):
                if(idx >0):
                    elements = self.driver.find_elements_by_xpath("//li[@class='D(ib) Mstart(8px)']")
                    elements[idx].click()
                    self.soup = BeautifulSoup(self.driver.page_source,"html.parser")
                    self.parse_html()
                    self.parse_stats(data,append=True)
                    self.driver.refresh()


    def get_html_table_attr(self):
        if self.status > 0:
            print("Rows:",len(self.rows))
        else:
            print("Please Parse Html")

    


class PlayerStatistics:

    def __init__(self) -> None:
        self.tables = {}
        self.table_IDS = ['Passing','Rushing','Receiving','Kicking','Kickoffs','Punting','Returns','Defense']
    
    def add_table(self,name,df):
        self.tables[name] = df
    
    def get_all_tables(self,scraper: Scraper,base_url):
        scraper.create_driver()
        for i,name in enumerate(self.table_IDS):
            url = base_url[0] + str(i) + base_url[1]
            scraper.set_url(url, name)
            scraper.parse_url()
            scraper.parse_html()
            scraper.parse_all_stats(self)
        
        scraper.close_driver()
    
    def save_tables_to_pickle(self,loc: str):
        pickle_out = open(loc, 'wb')
        pickle.dump(self.tables, pickle_out)
        pickle_out.close()

    def load_in_tables_from_pickle(self,loc: str) -> dict:
         # create new dictionary from pickle file
        pickle_in = open(loc, 'rb')
        new_dict = pickle.load(pickle_in)

        return new_dict



def main():
    sc1 = Scraper()
    pc1 = PlayerStatistics()
    base_url = ["https://sports.yahoo.com/nfl/stats/weekly/?sortStatId=PASSING_YARDS&selectedTable=","&week={%22week%22:19,%22seasonPhase%22:%22POSTSEASON%22}"]
    pc1.get_all_tables(sc1,base_url)
    pc1.save_tables_to_pickle('pc1_tables_dict.pickle')

    pc1.tables = pc1.load_in_tables_from_pickle('pc1_tables_dict.pickle')
    
    # print(pc1.tables['Passing'])
    # print(pc1.tables['Receiving'])
    # print(pc1.tables['Defense'])


    #Load into Cockroach DB
    db_connection = DatabaseConnection()
    db_connection.create_connection()
    db_connection.execute_statement('SELECT * FROM sample')

    print(db_connection.result)







if __name__ == "__main__":
    main()




# source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()


