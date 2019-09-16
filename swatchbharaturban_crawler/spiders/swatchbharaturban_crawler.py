# -*- coding: utf-8 -*-
import scrapy
import requests 

class SwatchbharaturbanCrawlerSpider(scrapy.Spider):
	# name of the spider
	name = "swatchbharaturban_crawler"
	# the domains where the spider is allowed to crawl
	allowed_domains = ["swachhbharaturban.gov.in"]
	# the url where the spider with start crawling 
	start_urls = ['http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx']
	# delay before downoadig a web page 
	download_delay = 1
	

	# path to dave data
	data_dir_path = "./swatchbharaturban_crawler/data/"
	raw_dir_path = "./swatchbharaturban_crawler/data/"
	
	# file name to save data
	filename = "swatchbharat_data.csv"
	
	# url to push the updated data 
	url = None
	
	# custom setting to write the output in a file
	custom_settings = {
		# fields to be written
		'FEED_EXPORT_FIELDS': [
			"State",
			"District",
			"ULB Name",
			"Ward",
			"No. of Applications Received",
			"No. of Applications Not Verified",
			"No. of Applications Verified",
			"No. of Applications Approved",
			"No. of Applications Approved having Aadhar No.",
			"No. of Applications Rejected",
			"No. of Applications Pullback",
			"No. of Applications Closed",
			"No. of Constructed Toilet Photo",
			"No. of Commenced Toilet Photo",
			"No. of Constructed Toilet Photo through Swachhalaya",
		],      
		# format in which the output should be saved
		'FEED_FORMAT': 'csv',
		# the file path and name to store the data
		'FEED_URI': data_dir_path+filename,
	}       

	def parse(self, response):
		'''
		This function is called by default and the crawling starts from here only.
		This function crawls and list down all the states.
		This function then calls the parse_district function in order to crawl the districts of the state.
		'''
		
		# iterate over the list made by this css selector to get the list of all states
		for state in response.css('a.lnkButton'):

			# to get the target value, to be passed in the form request
			target=state.css("::attr(href)").extract_first().split("'")[1]
			# to get the state name
			state_name=state.css("::text").extract_first()

			# for every state, a FormRequest would be made to extract districts of the state
			yield scrapy.FormRequest(
				# url where the request would be sent
				'http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx',
				
				# data to be sent along with form
				formdata={
					# state_name
					'state': state_name,
					# information along with target value would be sent
					'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$uppnlApplication_id|'+target,
					# the target value extracted above would be sent
					'__EVENTTARGET': target,
					'__EVENTARGUMENT': '' , 
					'__LASTFOCUS': '',
					#  the VIEWSTATE would be extracted and that would be passes along with the form ..... property of APS.NET sites
					'__VIEWSTATE': response.css('input#__VIEWSTATE::attr(value)').extract_first(),
					# the VIEWSTATEGENERATOR is also the same as VIEWSTATE
					'__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first() , 
					'__VIEWSTATEENCRYPTED': '', 
					'ctl00$hidden1': '',
					'ctl00$ddlLanguage': 'en-US',
					'ctl00$ContentPlaceHolder1$HiddenField1': '', 
					'ctl00$ContentPlaceHolder1$hdnDetail': '',
					'__ASYNCPOST': 'false'
				},
				
				# now the parse_districts would be called, in order crawl over the districts of the state
				callback=self.parse_districts
			)

		# after the crawling is complete, data is uploaded to the url specified
		self.send_data()


	def parse_districts(self,response):
		'''
		This function is called by parse() funtion which is used to crwl to crwl over the state.
		For every state, parse_dictionary() function would be called to crawl over all the districts of a state.
		This function then calls the parse_ulb function in order to crawl the ULB of the District.
		'''
		
		# iterate over the list made by this css selector to get the list of all districts 
		for district in response.css('a.lnkButton')[1:]:
			
			# to get the updated target value, to be passed in the form request
			target=district.css("::attr(href)").extract_first().split("'")[1]
			# to get the district name
			district_name=district.css("::text").extract_first()
			
			# for every district, a FormRequest would be made to extract ULB of the district ...here only the new information would be added
			yield scrapy.FormRequest.from_response(
				# would be taking the info from the previous response we had
				response,

				# the data which needs to be updated to be sent along with form
				formdata={
					# information along with target value would be sent
					'ctl00$ScriptManager1':'ctl00$ContentPlaceHolder1$uppnlApplication_id|'+target,
					# refreshing the EVENTTARGET with the updated value 
					'__EVENTTARGET':target,
					'ctl00$hidden1':'',
					'ctl00$ContentPlaceHolder1$HiddenField1':'', 
					'ctl00$ContentPlaceHolder1$hdnDetail':'', 
					# the district name would also be sent along with the request
					'district': district_name,
				},
				
				# now the parse_ulb would be called, in order crawl over the ULB of the District
				callback=self.parse_ulb,
			)
	
	def parse_ulb(self,response):
		'''
		This function is called by parse_district() funtion which is used to crawl over the districts.
		For every district, parse_ulb() function would be called to crawl over all the ULB of a district.
		This function then calls the parse_ward() function in order to crawl the Ward of the ULB.
		'''
		
		# iterate over the list made by this css selector to get the list of all ULB 
		for ulb in response.css('a.lnkButton')[2:]:

			# to get the updated target value, to be passed in the form request
			target=ulb.css("::attr(href)").extract_first().split("'")[1]
			# to get the ULB name
			ulb_name=ulb.css("::text").extract_first()
			
			# for every ULB, a FormRequest would be made to extract Ward of the ULB ...here only the new information would be added in the FormRequest
			yield scrapy.FormRequest.from_response(
				# would be taking the info from the previous response we had
				response,

				# the data which needs to be updated to be sent along with form
				formdata={
					# information along with target value would be sent
					'ctl00$ScriptManager1':'ctl00$ContentPlaceHolder1$uppnlApplication_id|'+target,
					# refreshing the EVENTTARGET with the updated value 
					'__EVENTTARGET':target,
					'ctl00$hidden1':'',
					'ctl00$ContentPlaceHolder1$HiddenField1':'', 
					'ctl00$ContentPlaceHolder1$hdnDetail':'', 
					# the ULB name would also be sent along with the request
					'ulb': ulb_name,
				},

				# now the parse_ward would be called, in order crawl over the Ward of the ULB
				callback=self.parse_ward,
			)
	
	def parse_ward(self,response):
		'''
		This function is called by parse_ulb() funtion which is used to crawl over the ULB.
		For every district, parse_ulb() function would be called to crawl over all the Wards of a ULB.
		This is the lowest Level of the Data, all the data would be stored here in this function.
		'''

		# this css selector would be used to get the list of various names defined on the page
		name_list=response.css("a.lnkButton::text").extract()
		
		# get the info from the name_list
		state_name=name_list[0]
		district_name=name_list[1]
		ulb_name=name_list[2]
		
		# this xpath selector would be used to select all the rows i.e the complete ward row 
		table=response.xpath("//span[contains(@id,'WARD_NO')]/../..")
		
		# iterate over the tabel rows to get the information about evry ward
		for row in table:

			# making dictonary for evry row
			item= {
				# state name ... extracted earlier only
				"State":state_name,
				# district name ... extracted earlier only
				"District":district_name,
				# ULB name ... extracted earlier only
				"ULB Name":ulb_name,
				# Ward name ... extracting using CSS selector ... the cell that contains 'WARD_NO' in the id
				"Ward":row.css("[id*='WARD_NO']::text").extract_first(),
				# Ward name ... extracting using CSS selector ... the cell that contains 'WARD_NO' in the id
				"No. of Applications Received":row.css("[id*='APP_RECEIVED']::text").extract_first(),
				# Applications Not Verified ... extracting using CSS selector ... the cell that contains 'APP_VERIFIEDNOT' in the id
				"No. of Applications Not Verified":row.css("[id*='APP_VERIFIEDNOT']::text").extract_first(),
				# Applications Verified ... extracting using CSS selector ... the cell that contains 'APP_VERIFIED' in the id
				"No. of Applications Verified":row.css("[id*='APP_VERIFIED']::text").extract_first(),
				# Applications Approved ... extracting using CSS selector ... the cell that contains 'APP_APPROVED' in the id
				"No. of Applications Approved":row.css("[id*='APP_APPROVED']::text").extract_first(),
				# Applications Approved having Aadhar No. ... extracting using CSS selector ... the cell that contains 'APP_APPROVED_AADHAR' in the id
				"No. of Applications Approved having Aadhar No.":row.css("[id*='APP_APPROVED_AADHAR']::text").extract_first(),
				# Applications Rejected ... extracting using CSS selector ... the cell that contains 'APP_REJECTED' in the id
				"No. of Applications Rejected":row.css("[id*='APP_REJECTED']::text").extract_first(),
				# Applications Pullback ... extracting using CSS selector ... the cell that contains 'APP_PULLBACK' in the id
				"No. of Applications Pullback":row.css("[id*='APP_PULLBACK']::text").extract_first(),
				# Applications Closed ... extracting using CSS selector ... the cell that contains 'APP_CLOSED' in the id
				"No. of Applications Closed":row.css("[id*='APP_CLOSED']::text").extract_first(),
				# Constructed Toilet Photo ... extracting using CSS selector ... the cell that contains 'APP_CTP' in the id
				"No. of Constructed Toilet Photo":row.css("[id*='APP_CTP']::text").extract_first(),
				# Commenced Toilet Photo ... extracting using CSS selector ... the cell that contains 'APP_INTER' in the id
				"No. of Commenced Toilet Photo":row.css("[id*='APP_INTER']::text").extract_first(),
				# Constructed Toilet Photo through Swachhalaya ... extracting using CSS selector ... the cell that contains 'APP_CTSWACHHALAYA' in the id
				"No. of Constructed Toilet Photo through Swachhalaya":row.css("[id*='APP_CTSWACHHALAYA']::text").extract_first(),
			}
			yield item

		
	def send_data(self):
		'''
		This function is used to send data after the crawling is comlete
		'''

		# check if the url is not None
		if(self.url is not None):
			# open the file and POST it over the url
			with open('../data/swatchbharat_data.csv', 'rb') as f:
				requests.post(self.url, data=f)