# -*- coding: utf-8 -*-
import scrapy
import requests 

class SwatchbharatViewstateSpider(scrapy.Spider):
	name = "swatchbharat_viewstate"
	allowed_domains = ["swachhbharaturban.gov.in"]
	start_urls = ['http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx']
	data_dir_path="../data/"
	raw_dir_path="../data/"
	filename="swatchbharat_data.csv"
	url=None
	
	custom_settings = {
		'FEED_EXPORT_FIELDS' : ['state', 'district', 'ulb', 'ward'],      
		'FEED_FORMAT': 'csv',
		'FEED_URI': data_dir_path+filename,
	}		

	def parse(self, response):
		for state in response.css('a.lnkButton'):
			target=state.css("::attr(href)").extract_first().split("'")[1]
			state_name=state.css("::text").extract_first()
			yield scrapy.FormRequest(
				'http://swachhbharaturban.gov.in/ihhl/RPTApplicationSummary.aspx',
				formdata={
					'state':state_name,
					'ctl00$ScriptManager1': 'ctl00$ContentPlaceHolder1$uppnlApplication_id|'+target,
					'__EVENTTARGET': target,
					'__EVENTARGUMENT': '' , 
					'__LASTFOCUS': '',
					'__VIEWSTATE':response.css('input#__VIEWSTATE::attr(value)').extract_first(),
					'__VIEWSTATEGENERATOR': response.css('input#__VIEWSTATEGENERATOR::attr(value)').extract_first() , 
					'__VIEWSTATEENCRYPTED': '', 
					'ctl00$hidden1': '',
					'ctl00$ddlLanguage': 'en-US',
					'ctl00$ContentPlaceHolder1$HiddenField1': '', 
					'ctl00$ContentPlaceHolder1$hdnDetail': '',
					'__ASYNCPOST': 'false'
				},
				callback=self.parse_districts
				)

	def parse_districts(self,response):
		for district in response.css('a.lnkButton')[1:]:
			target=district.css("::attr(href)").extract_first().split("'")[1]
			district_name=district.css("::text").extract_first()
			yield scrapy.FormRequest.from_response(
				response,
				formdata={
					'ctl00$ScriptManager1':'ctl00$ContentPlaceHolder1$uppnlApplication_id|'+target,
					'__EVENTTARGET':target,
					'ctl00$hidden1':'',
					'ctl00$ContentPlaceHolder1$HiddenField1':'', 
					'ctl00$ContentPlaceHolder1$hdnDetail':'', 
					'district': district_name,
				},
				callback=self.parse_ulb,
				)
	
	def parse_ulb(self,response):
		for ulb in response.css('a.lnkButton')[2:]:
			target=ulb.css("::attr(href)").extract_first().split("'")[1]
			ulb_name=ulb.css("::text").extract_first()
			yield scrapy.FormRequest.from_response(
				response,
				formdata={
					'ctl00$ScriptManager1':'ctl00$ContentPlaceHolder1$uppnlApplication_id|'+target,
					'__EVENTTARGET':target,
					'ctl00$hidden1':'',
					'ctl00$ContentPlaceHolder1$HiddenField1':'', 
					'ctl00$ContentPlaceHolder1$hdnDetail':'', 
					'ulb': ulb_name,
				},
				callback=self.parse_ward,
				)
	
	def parse_ward(self,response):
		self.log(">>>>>>>I am Ironman<<<<<<<<<<	")
		name_list=response.css("a.lnkButton::text").extract()
		state_name=name_list[0]
		district_name=name_list[1]
		ulb_name=name_list[2]
		wards_list=response.css("[id*='WARD_NO']::text").extract()
		for ward in wards_list:
			yield {
				"state":state_name,
				"district":district_name,
				"ulb":ulb_name,
				"ward":ward
			}