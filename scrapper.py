import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import dateparser

class WebScrapperModule:
    authors = []
    urls = []
    dates = []
    headlines = []
    ids = []

    def web_scrap_articles_from_the_link(self, URL):

        response = requests.get(URL)

        text_file = open("D:/data.txt", "w")
 
        text_file.write(response.text)
        
        if response.status_code != 200:
            return "Error in fetching data"
    
        soup = BeautifulSoup(response.content, features="html.parser")
        id = 1

        # scrap the articles present in top right and the main one section
        
        top_right_and_main_articles = soup.findAll("div", {'class': "max-w-content-block-standard md:w-content-block-compact md:max-w-content-block-compact lg:w-[240px] lg:max-w-[240px] lg:pr-10"})
        for head_url in top_right_and_main_articles:
            href_tags = head_url.find("a", {'class': "group-hover:shadow-underline-franklin"})
            headline = href_tags.string
            url = URL + href_tags["href"]
            author_class = head_url.find("a", {'class': "text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8"})
            author = author_class.string
            date_class = head_url.find("span", {'class': "text-gray-63 dark:text-gray-94"})
            date = dateparser.parse(str(date_class.string)).strftime('%d-%m-%Y')
            self.authors.append(author)
            self.urls.append(url)
            self.dates.append(date)
            self.headlines.append(headline)
            self.ids.append(id)
            id+=1
        
        # end

        # scrap the articles present in the lower left section

        # lower_left_articles = soup.findAll("div",{'class': "duet--content-cards--content-card relative flex flex-row border-b border-solid border-gray-cc px-0 last-of-type:border-b-0 dark:border-gray-31 py-16 hover:bg-[#FBF9FF] dark:hover:bg-gray-18 max-w-container-sm last-of-type:border-b-0 md:px-10 lg:py-24"})

        # end
        
        data = {
                "id":self.ids,
                "URL":self.urls,
                "headline":self.headlines,
                "author":self.authors,
                "date":self.dates
            }
        
        now = datetime.now()
        todays_date = now.strftime('%d-%m-%Y')
        file_name = 'D:/' + todays_date + '_verge.csv'

        csv_data = pd.DataFrame.from_dict(data)
        csv_data.to_csv(file_name, header=True, index=False)

if __name__ == '__main__':
    web_scrapper_object = WebScrapperModule()
    web_scrapper_object.web_scrap_articles_from_the_link("https://www.theverge.com")
