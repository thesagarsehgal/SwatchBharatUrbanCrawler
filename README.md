# Swatch Bharat Urban Crawler

This is a crawleer that crawls the complete website  http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx and extracts the complete information.

### About 

- This crawler was build as a task for ATLAN.
- The complete data from the website was crawled and stored in a single file
- This was a new task and learned how to scrap the ASP.NET websites. (Used the https://blog.scrapinghub.com/2016/04/20/scrapy-tips-from-the-pros-april-2016-edition for refrence).
- Also at the end of complete data scrapping, a POST request would be made to the `URL` specified.
- For making the post request every 5 minutes, we can put the project in the Scrapinghub, and schedule it to crawl every 5 minutes. 
- On completing the crawling, the data would automatically posted.
- Also the setup.py file has also been added. 

### How to Setup

1. Clone the repository
```
git clone https://github.com/sagar-sehgal/SwatchBharaturban_Crawler
```
2. Install the dependencies
```
pip install -r requirements.txt
```
3. Run the Crawler
```
scrapy crawl swatchbharaturban_crawler
```

The crawled data would be stored in the `swatchbharaturban_crawler/data/swatchbharat_data.csv` file.

