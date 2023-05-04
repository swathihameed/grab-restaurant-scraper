import csv
import json
import os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time

class GrabScraper():

    def __init__(self):
        self.current_path = os.getcwd()
        self.url = 'https://food.grab.com/ph/en/restaurants'
        self.driver_path = os.path.join(os.getcwd(), 'chromedriver')
        self.driver = webdriver.Chrome(executable_path = self.driver_path)
        self.driver.implicitly_wait(30)
        self.base_url = "https://food.grab.com/ph/en/restaurants"
        self.headers = {
            'authority': 'food.grab.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'cookie': 'gfc_country=PH; gfc_session_guid=9c8d7ad0-ec25-41d7-aa3b-edbdebaabaa0; pid=www.google.com; c=non-paid; next-i18next=en; _gsvid=e3acb77e-ab6d-469e-abc0-b8c0f492350f; _gcl_au=1.1.792499045.1683121784; _gid=GA1.2.2081205670.1683121784; _fbp=fb.1.1683121784636.101239079; hwuuid=71e1f7da-cb8c-47ea-97c9-a2d0d2cbd43d; hwuuidtime=1683121825; _hjSessionUser_1532049=eyJpZCI6IjUxZDcxNGYyLTVhZWItNTJkOS04NjlhLTYyODZlMTM0ZDcxNiIsImNyZWF0ZWQiOjE2ODMxMjE3ODQyOTEsImV4aXN0aW5nIjp0cnVlfQ==; _hjSessionUser_1740618=eyJpZCI6IjgzMTM0MWQ3LTliMGItNTQ1YS1hMDU5LTg4Zjc2Zjc3ZTM0ZSIsImNyZWF0ZWQiOjE2ODMxMjIxNTk0ODAsImV4aXN0aW5nIjp0cnVlfQ==; location=%7B%22id%22%3A%22IT.2JUVPWBDH04AD%22%2C%22latitude%22%3A14.592859%2C%22longitude%22%3A120.971903%2C%22address%22%3A%22Sta.%20Clara%20St.%2C%20Brgy.%20656%2C%20Intramuros%2C%20Manila%20City%2C%20Metro%20Manila%2C%20NCR%2C%201002%22%2C%22countryCode%22%3A%22PH%22%2C%22isAccurate%22%3Atrue%2C%22addressDetail%22%3A%22Fort%20Santiago%20Main%20Entrance%20-%20Sta.%20Clara%20St.%2C%20Brgy.%20656%2C%20Intramuros%2C%20Manila%20City%2C%20Metro%20Manila%2C%20NCR%2C%201002%22%2C%22noteToDriver%22%3A%22%22%2C%22city%22%3A%22Metro%20Manila%22%2C%22cityID%22%3A4%2C%22displayAddress%22%3A%22Fort%20Santiago%20Main%20Entrance%20-%20Sta.%20Clara%20St.%2C%20Brgy.%20656%2C%20Intramuros%2C%20Manila%20City%2C%20Metro%20Manila%2C%20NCR%2C%201002%22%7D; OptanonAlertBoxClosed=2023-05-03T15:43:21.555Z; _ga=GA1.2.38872989.1683121784; OptanonConsent=isGpcEnabled=0&datestamp=Wed+May+03+2023+21%3A13%3A47+GMT%2B0530+(India+Standard+Time)&version=202303.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=IN%3BKA&AwaitingReconsent=false; _gssid=2304031625-azit98pfi5s; _gat_UA-73060858-24=1; _hjAbsoluteSessionInProgress=0; _ga_RPEHNJMMEM=GS1.1.1683131121.4.1.1683131122.59.0.0; gfc_country=PH; next-i18next=en',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
        }

    def interceptor(self,request):
        request.headers =  self.headers

    def page_load(self):
        """
        Load the url in the driver
        """
        driver = self.driver
        driver.request_interceptor = self.interceptor 
        delay = 3
        driver.get(self.base_url)
        for i in range(1,2):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
        html_source = driver.page_source
        data = html_source.encode('utf-8')
        # self.create_csv_file()
        # self.get_lat_long_data(driver)

    def scrape_data(self):
        """
        Scrape the lat/long data from the page
        """
        script_element = self.driver.find_elements(By.TAG_NAME,"script")
        for element in script_element:
            if element.get_attribute("id") == '__NEXT_DATA__':
                content_element = element
        if content_element:
            content = json.loads(content_element.get_attribute("innerHTML"))
            if content:
                try:
                    restaurant_list = content["props"]["initialReduxState"]["pageRestaurantsV2"]["entities"]["restaurantList"]
                    for k,v in restaurant_list.items():
                        self.mycsv.writerow({"Name": v["name"], "Latitude": v["latitude"], "Longitude":v["longitude"]})
                except:
                    pass

    def create_csv_file(self):
        rowHeaders = ["Name", "Latitude", "Longitude"]
        self.file_csv = open('Grab_restaurant_list.csv', 'w', newline='', encoding='utf-8')
        self.mycsv = csv.DictWriter(self.file_csv, fieldnames=rowHeaders)
        self.mycsv.writeheader()

    def tearDown(self):
        self.driver.quit()
        self.file_csv.close()

if __name__ == "__main__":
    GrabScraper = GrabScraper()
    GrabScraper.page_load()
    GrabScraper.create_csv_file()
    GrabScraper.scrape_data()
    GrabScraper.tearDown()
    print('task_completed')
