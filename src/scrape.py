from email import header
import select
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException        
import pickle
from connect_to_db import DatabaseConnection
from selenium.webdriver.support.ui import Select
# from cleaning_pickle import update_tables


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

        # html_table = self.soup.find("table",{"class":"table graph-table W(100%) Ta(start) Bdcl(c) Mb(56px) Ov(h)"})
        html_table = self.driver.find_element_by_xpath("//table[@class='table graph-table W(100%) Ta(start) Bdcl(c) Mb(56px) Ov(h)']")
        
        is_header = True
        for row in html_table.find_elements_by_tag_name("tr"):
            if is_header:
                self.header = row
                is_header = False
            else:
                self.rows.append(row)


        # for row in html_table.findAll("tr"):
        #     if is_header:
        #         self.header = row
        #         is_header = False
        #     else:
        #         self.rows.append(row)

        self.status += 1
    def parse_stats(self, data: 'PlayerStatistics', append=False):
        headers_list = list()
        stats_list = list()
        for col in self.header.find_elements_by_tag_name("th"):
            headers_list.append(col.get_attribute('title'))
        
        for row in self.rows:
            ind_stats = list()
            for col in row.find_elements_by_tag_name("th"):
                ind_stats.append(col.text)
            for col in row.find_elements_by_tag_name("td"):
                if is_num_or_float(col.text):
                    ind_stats.append(float(col.text))
                else:
                    if(col.text == '-'):
                        ind_stats.append(0.0)
                    else:
                        ind_stats.append(col.text)

            #Add row
            stats_list.append(ind_stats)

        # for col in self.header.findAll("th"):
        #     headers_list.append(col["title"])
        
        # for row in self.rows:
        #     ind_stats = list()
        #     for col in row.findAll("th"):
        #         ind_stats.append(col.text)
        #     for col in row.findAll("td"):
        #         if is_num_or_float(col.text):
        #             ind_stats.append(float(col.text))
        #         else:
        #             if(col.text == '-'):
        #                 ind_stats.append(0.0)
        #             else:
        #                 ind_stats.append(col.text)

        #     #Add row
        #     stats_list.append(ind_stats)
        
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
            self.select_week(self.curr_week)
            elements = self.driver.find_elements_by_xpath("//li[@class='D(ib) Mstart(8px)']")
            # print(len(elements))
        except NoSuchElementException:
            print("Not Found")
            isMore = False

        if isMore:
            for idx in range(len(elements)):
                if(idx >0):
                    print("On Page: ",idx+1,"Out of: ",len(elements))
                    self.select_week(self.curr_week)
                    elements = self.driver.find_elements_by_xpath("//li[@class='D(ib) Mstart(8px)']")
                    # print("now there is ",len(elements))
                    elements[idx].click()
                    self.soup = BeautifulSoup(self.driver.page_source,"html.parser")
                    self.parse_html()
                    self.parse_stats(data,append=True)
                    # self.driver.refresh()

    def select_week(self,week):
        select = Select(self.driver.find_elements_by_xpath("//select[@class='Bgc(#fff)! C(#000)! Cur(p) M(0) P(0) Pos(a) T(0) Start(0) W(100%) H(100%) Op(0)']")[1])
        # print(select.first_selected_option.text)
        # select by value 
        select.select_by_visible_text('WEEK '+str(week))
        self.curr_week = week

        self.soup = BeautifulSoup(self.driver.page_source,"html.parser")
        # select.select_by_index(week)


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
        full_tables = []
        weeks = [19,20]

        for week in weeks:
            for i,name in enumerate(self.table_IDS):
                url = base_url[0] + str(i) + base_url[1] + str(week) + base_url[2]
                scraper.set_url(url, name)
                scraper.parse_url()
                scraper.select_week(week)
                scraper.parse_html()
                scraper.parse_all_stats(self)

            self.update_tables()
            # print(self.tables['Passing'])
            full_tables.append(self.tables)
            self.tables={}

        #Combine all Tables..
        self.combine_all_weeks(full_tables)

        scraper.close_driver()
    
    def combine_all_weeks(self,full_tables):
        final_tables = {}

        for key in full_tables[0]:
            #Merge all
            for i in range(len(full_tables)):
                if key in final_tables:
                    # print(full_tables[i][key])
                    final_tables[key] = pd.concat([final_tables[key], full_tables[i][key]]).groupby(['Player','Team']).sum().reset_index()
                else:
                    # print(full_tables[i][key])
                    final_tables[key] = full_tables[i][key]

        print(final_tables['Passing'])

        self.tables = final_tables





    def update_tables(self):
        # starts by loading pickle from scrape.py
        # pc1.tables = pc1.load_in_tables_from_pickle('pc1_tables_dict.pickle')
        defense_players = self.tables['Defense']
        passing_players = self.tables['Passing']
        rushing_players = self.tables['Rushing']
        #print(df['Fumbles returned for a touchdown'])
        # need to add support for fumbes returned for touchdown
        self.tables['TeamDefense'] = defense_players.groupby(defense_players['Team']).agg({'Sacks':'sum','Interceptions':'sum','Interception Return Touchdowns':'sum','Forced Fumbles':'sum','Safeties':'sum','Fumbles returned for a touchdown':'sum'})
        self.tables['TeamOffense'] = pd.merge(passing_players.groupby(passing_players['Team']).agg({'Passing Yards':'sum'}), rushing_players.groupby(rushing_players['Team']).agg({'Rushing Yards':'sum'}), on='Team')
        # print(self.tables['TeamOffense'])

        self.tables['TeamDefense'] = self.tables['TeamDefense'].reset_index()
        self.tables['TeamOffense'] = self.tables['TeamOffense'].reset_index()
        
        self.tables['TeamDefense'] = self.tables['TeamDefense'].rename(columns={'Team': 'Player'})
        self.tables['TeamOffense'] = self.tables['TeamOffense'].rename(columns={'Team': 'Player'})
        self.tables['TeamDefense']['Team'] = self.tables['TeamDefense']['Player']
        self.tables['TeamOffense']['Team'] = self.tables['TeamOffense']['Player']

    def save_tables_to_pickle(self,loc: str):
        pickle_out = open(loc, 'wb')
        pickle.dump(self.tables, pickle_out)
        pickle_out.close()

    def load_in_tables_from_pickle(self,loc: str) -> dict:
         # create new dictionary from pickle file
        pickle_in = open(loc, 'rb')
        new_dict = pickle.load(pickle_in)

        return new_dict

    def load_tables_to_sql(self,db_connection :DatabaseConnection):
        for name in self.tables:
            df = self.tables[name]
            # db_connection.execute_statement("COPY sample_table_name FROM ./temp.csv DELIMITER ',' CSV_HEADER")
            df = df.loc[:,~df.columns.duplicated()]
            df.to_sql(name, db_connection.conn, if_exists='replace', index = False)


def main():
    sc1 = Scraper()
    pc1 = PlayerStatistics()
    #base_url = ["https://sports.yahoo.com/nfl/stats/weekly/?sortStatId=PASSING_YARDS&selectedTable=","&week={'week':",",'seasonPhase':'POSTSEASON'}"]
    #pc1.get_all_tables(sc1,base_url)

    #pc1.save_tables_to_pickle('pc1_tables_dict.pickle')

    # #Optional Loading from File
    pc1.tables = pc1.load_in_tables_from_pickle('pc1_tables_dict.pickle')
    
    # #Load into SQLLite3
    db_connection = DatabaseConnection()
    db_connection.create_connection()
    pc1.load_tables_to_sql(db_connection)

    db_connection.execute_statement('SELECT * FROM Passing')
    # db_connection.execute_statement("SELECT name FROM sqlite_master WHERE type='table'")

    print(db_connection.result)

    db_connection.close_connection()



if __name__ == "__main__":
    main()




# source = urllib.request.urlopen('https://pythonprogramming.net/parsememcparseface/').read()


