import scrapy
from scrapy.crawler import CrawlerProcess,CrawlerRunner
from scrapy.selector import Selector
from scrapy.exceptions import CloseSpider
import csv
import os
from multiprocessing.context import Process
from scrapy.exceptions import CloseSpider
from twisted.internet import protocol, reactor, endpoints
class VinSpider(scrapy.Spider):
    name='input_vin'
    list_result=[]
    url_vin='https://vpic.nhtsa.dot.gov/decoder/Decoder'
    headers={
            ":authority": "vpic.nhtsa.dot.gov",
            ":method": "POST",
            ":path": "/decoder/Decoder",
            ":scheme": "https",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,vi;q=0.8",
            "cache-control": "no-cache",
            "content-length": "168",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": "__RequestVerificationToken_L2RlY29kZXI1=AudhXnQmG2N1e8CYT9M0Ekv0utlwMkVCOv5MczmNuBZIdcodV6r5hIsmDG9XIibttohBKsOJ9ashAPBtD3Lnmc-1lYuYFbpaDHImLhQDsOg1; ASP.NET_SessionId=ngcgjhuds2ecgn5bazdtsu1i",
            "origin": "https://vpic.nhtsa.dot.gov",
            "pragma": "no-cache",
            "referer": "https://vpic.nhtsa.dot.gov/decoder",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
    }
    ListVin=[]
    start_urls=['https://vpic.nhtsa.dot.gov/decoder']
    def parse(self,response):
        token = response.css('input[name="__RequestVerificationToken"]::attr(value)').extract_first()
        Pathfile='input_VIN.txt'   
        with open(Pathfile,'r') as f:
            data=f.readlines()
        for a in data:
            self.ListVin.append(a)        
        data={
            "__RequestVerificationToken":"",
            "VIN":"",
            "ModelYear":""      
        }
        if(len(self.ListVin)>0):
            for Vin in self.ListVin:
                token = response.css('input[name="__RequestVerificationToken"]::attr(value)').extract_first()
                data={
                    '__RequestVerificationToken':token,
                    'VIN':Vin.strip(),
                    'ModelYear':''        
                }
                yield scrapy.FormRequest(url=self.url_vin,formdata=data,callback=self.parse_Vin)              
    def parse_Vin(self,response):
        hsx=Selector(response)
        root=os.getcwd()
        vehicle={'Vin':' ','Man':' ','VehType':' ','Year':' ','Make':' ','Model':' ','Bodyclass':' ','Series':' ','Cylinder':' ','Trim':' ','EngineModel':' ','FuelType':' ','EngineDisplacement':' '}      
        vehicle['Vin']=hsx.xpath("//input[@id='VIN']").attrib['value']
        vehicle['Man']=hsx.xpath("//body/div[@id='outerDiv']/div[@id='divCommonDetails']/div[@id='searchform']/div[1]/div[2]/div[2]/div[1]/p[1]/a[1]/text()").get()
        vehicle['VehType']=hsx.xpath("//body/div[@id='outerDiv']/div[@id='divCommonDetails']/div[@id='searchform']/div[1]/div[2]/div[2]/div[1]/p[3]/text()").get()
        vehicle['Year']=hsx.xpath("//span[@id='decodedModelYear']/text()").get()
        vehicle['Make']=hsx.xpath("//span[@id='decodedMake']/text()").get()
        vehicle['Model']=hsx.xpath("//span[@id='decodedModel']/text()").get()
        vehicle['Bodyclass']=hsx.xpath("//body/div[@id='outerDiv']/div[@id='divCommonDetails']/div[@id='searchform']/div[1]/div[2]/div[2]/div[1]/p[7]/text()").get()
        Series=hsx.xpath('//label[contains(text(),"Series:")]/following-sibling::text()').get()
        if((Series is None)==False):
            vehicle['Series']=Series.strip()
        vehicle['Cylinder']=hsx.xpath("//label[contains(text(),'Cylinders:')]/following-sibling::text()").get().strip()
        Trim=hsx.xpath("//label[contains(text(),'Trim:')]/following-sibling::text()").get()
        if((Trim is None)==False):
            vehicle['Trim']=Trim.strip()
        vehicle['EngineModel']=hsx.xpath("//label[contains(text(),'Engine Model:')]/following-sibling::text()").get().strip()
        vehicle['FuelType']=hsx.xpath("//label[contains(text(),' Primary Fuel Type:')]/following-sibling::text()").get().strip()
        vehicle['EngineDisplacement']=hsx.xpath("//label[contains(text(),' Engine Displacement (L):')]/following-sibling::text()").get().strip()
        self.list_result.append(vehicle)
        if(len(self.list_result) == len(self.ListVin)):
            filename = root+'\\result.csv'        
            with open(filename, 'w',newline="") as f:
                writer=csv.DictWriter(f,['Vin','Man','VehType','Year','Make','Model','Bodyclass','Series','Cylinder','Trim','EngineModel','FuelType','EngineDisplacement'])
                writer.writeheader()
                for dt in self.list_result:
                    writer.writerow(dt)            
    def run_Vin(VinSpider):      
        process=CrawlerProcess()
        process.crawl(VinSpider)
        process.start()
VinSpider.run_Vin(VinSpider)