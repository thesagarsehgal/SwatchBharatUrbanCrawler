# Swatch Bharat Urban Crawler

This is a crawler that crawls the complete website  http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx and extracts the complete information.

### About 

- This crawler was build as a task for ATLAN.
- The complete data from the website was crawled and stored in a single file
- This was a new task and learned how to scrap the ASP.NET websites which use `__VIEWSTATE` (Used the https://blog.scrapinghub.com/2016/04/20/scrapy-tips-from-the-pros-april-2016-edition as a tutorial on how to Crawl ASP.NET websites).
- Also at the end of complete data scrapping, a POST request would be made to the `URL` specified.
- Also, the setup.py file has been added. 
- The extracted file contains the following columns:-
    - State
    - District
    - ULB Name
    - Ward
    - No. of Applications Received
    - No. of Applications Not Verified
    - No. of Applications Verified 
    - No. of Applications Approved
    - No. of Applications Approved having Aadhar No.
    - No. of Applications Rejected
    - No. of Applications Pullback
    - No. of Applications Closed
    - No. of Constructed Toilet Photo
    - No. of Commenced Toilet Photo
    - No. of Constructed Toilet Photo through Swachhalaya

### Doubts/Assumptions

1. **DOUBT=>** How can we make a POST request every 5 minutes, since the data crawling itself takes a lot more of time.
  
  **ASSUMPTION=>** For making the post request every 5 minutes, we can put the project in the ScrapingHub, and schedule it to crawl every 5 minutes. The crawler has been made such that it would make a POST request on completing the crawling, and the data would automatically be posted.

2. **DOUBT=>** How many output files are required? Like 1 file containing all the information. Or the 4 Files containing information for 4 different levels like State, District, ULB and Ward Level.

  **ASSUMTIONS=>** I have made 1 CSV file only whose table was shown in the task containing all the information. Since all other information can be easily extracted from that file.


### How to Setup

1. Clone the repository
```
git clone https://github.com/sagar-sehgal/SwatchBharaturban_Crawler
```
2. Make a Virtual Environment
```
virtualenv venv --python=python3
```
3. Activate the virtualenv 
```
source venv/bin/activate
```
4. Change the Repository
```
cd SwatchBharaturban_Crawler
```
5. Install the dependencies
```
pip install -r requirements.txt
```
6. Run the Crawler
```
scrapy crawl swatchbharaturban_crawler
```


The crawled data would be stored in the `swatchbharaturban_crawler/data/swatchbharat_data.csv` file.

