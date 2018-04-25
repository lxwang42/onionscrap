# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.spiders import Spider
from onion.items import OnionItem
import random
import json
import subprocess
all_headers={'Host': 'pjaopjqvjk6be4wz.onion',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
default_cookies=[{'MARKET_SESSION':'jq0n0mum0sp62477aovie02ag1'},{'MARKET_SESSION':'2fsa616dlvu7mjdrfdqovtpeu6'},
  {'MARKET_SESSION':'0j1hep4fudc7rftm1d8kpdeka3'},{'MARKET_SESSION':'c4qknnaicmci8tq3v3d3kgn4q6'},
  {'MARKET_SESSION':'1p2kk46smdgatbt2qu1auj0fv4'},{'MARKET_SESSION':'ndq88qtg2gvp02e43ecnl1t5i4'},
  {'MARKET_SESSION':'k5s9u653974hjjk6a0971u9ca5'},{'MARKET_SESSION':'mcttg0upshsdo279v8351977k0'},
  {'MARKET_SESSION':'vf9vnpmnhcvfi1fse187601jk4'},{'MARKET_SESSION':'fhpilvv4t78r0hmb9dfnoenhn4'},
  {'MARKET_SESSION':'662ijhpar09nvmlfdiq5010805'},{'MARKET_SESSION':'5h3vdpnpr4k21l3l2ohfejkrm1'},
  {'MARKET_SESSION':'q8tkhe7t8urarsm8puqq7h8ki7'},{'MARKET_SESSION':'75ib8go372nn3ksu96s6j63hp3'},
  {'MARKET_SESSION':'t161gbl16557tvjhuvu74n0fa3'},{'MARKET_SESSION':'62r96icdv3o160hlhar68e4u03'},
  {'MARKET_SESSION':'kjfalbmnq1ucse3cu85rlbq577'},{'MARKET_SESSION':'5l0of5dtfpj4qkerdles287tp2'},
  {'MARKET_SESSION':'2gan2qn3k1lvhl5r5lg64dg324'},{'MARKET_SESSION':'1eatf167thebdlm1ksm2867je1'},
  {'MARKET_SESSION':'6g62uris923etd6scqa96hlf70'},{'MARKET_SESSION':'16ttgakhuba5950vil18h5etm1'},
  {'MARKET_SESSION':'07u2rcjc23ld36qvhe925tlel6'},{'MARKET_SESSION':'dvoma4mg3ki53a49p1qr7k1nj1'},
  {'MARKET_SESSION':'ulcd18esl0t1tbjevsg72hvmr3'},{'MARKET_SESSION':'nc88r7ehb6j26b55imkf2lunr6'},
  {'MARKET_SESSION':'u7ssgbn3629qqitutaadl3tvp0'},{'MARKET_SESSION':'amvmnv3ulvou19ugni7f3q7rm4'},
  {'MARKET_SESSION':'6sdfpej727ad7ilmfhfn404md3'},{'MARKET_SESSION':'fbjkl7ghv6li3m4v090odm3t40'},
  {'MARKET_SESSION':'l8u7tmjko47kg9m2cqdnlvrg24'},{'MARKET_SESSION':'7kka0qcu6it3v8c7mj7i10nqr2'},
  ]

class tesSpider(Spider):
  name = 'step2'
  all_cookies = default_cookies
  i = 0
  def start_requests(self):
    with open('/Users/Sean/scrapyproject/onion/all.json', 'r') as uu:
      data = json.load(uu)
      
    for item in data:
      if len(item['item_sales'])!=0:
        yield item
        self.i = self.i +1
        print(self.i)
      else:
        ipage_url = 'http://pjaopjqvjk6be4wz.onion' + item['item_link'].lstrip('.')
        yield Request(url=ipage_url, meta={'item_1':item, 'temp_url':ipage_url}, cookies=random.choice(self.all_cookies), headers=all_headers, callback=self.parse_ipage)

  def parse_ipage(self,response):
    item = response.meta['item_1']
    ipage_url = response.meta['temp_url']

    status = response.status
    captcha = response.xpath('//div[@class="ddos"]/text()').extract()
    notfound = response.xpath('//img[@alt="Not found"]').extract()
    addtocart = response.xpath('//input[@value="Add to cart"]').extract()

    self.doerrors(item, status, ipage_url, notfound, captcha, addtocart)

    if notfound:
      item['item_sales'] = 'Page 404'
      yield item
      self.i = self.i +1
      print(self.i)
    else:
      item['item_sales'] = response.xpath('.//td[@class="age dontwrap"]/text()').extract()
      
      c0 = response.xpath('.//div[@class="category  selected  depth0"]/a/@href').extract()
      c1 = response.xpath('.//div[@class="category  selected  depth1"]/a/@href').extract()
      c2 = response.xpath('.//div[@class="category  selected  depth2"]/a/@href').extract()
      c3 = response.xpath('.//div[@class="category  selected  depth3"]/a/@href').extract()
      c4 = response.xpath('.//div[@class="category  selected  depth4"]/a/@href').extract()
      if c4:
        item['item_category'] = c4[0].split('=')[1]
      elif c3:
        item['item_category'] = c3[0].split('=')[1]
      elif c2:
        item['item_category'] = c2[0].split('=')[1]
      elif c1:
        item['item_category'] = c1[0].split('=')[1]
      elif c0:
        item['item_category'] = c0[0].split('=')[1]
      else:
        yield Request(url = ipage_url,meta={'item_1':item,'temp_url':ipage_url}, cookies=random.choice(self.all_cookies), headers=all_headers,  callback=self.parse_ipage, dont_filter= True)

      if not item['item_sales']:
        item['item_sales'] = 'Zero Sales'

      yield item
      self.i = self.i +1
      print(self.i)

  def doerrors(self, status, item, ipage_url, notfound, captcha, addtocart):
    
    if captcha:
      self.alarm()
      wait = input('又双叒叕要输入验证码了！')
      print("登录中")
      yield Request(url = ipage_url,meta={'item_1':item,'temp_url':ipage_url}, cookies=random.choice(self.all_cookies), headers=all_headers,  callback=self.parse_ipage, dont_filter= True)
    elif not addtocart:
      self.alarm()
      wait = input('网站可能无法访问')
      print("登录中")
      if wait=='n':
        item['item_sales'] = 'Page 404'
        yield item
        self.i = self.i +1
        print(self.i)
      else:
        print('更新cookies\n')
        self.all_cookies = []
        print('需要多少cookies\n')
        n_cookies = int(input())
        for i in range(n_cookies):
          self.all_cookies.append({'MARKET_SESSION':input("输入cookie")})
        yield Request(url = ipage_url,meta={'item_1':item,'temp_url':ipage_url}, cookies=random.choice(self.all_cookies), headers=all_headers,  callback=self.parse_ipage, dont_filter= True)
  
  def alarm(self):
    audio_file = "/Users/Sean/Downloads/cartoon002.wav" 
    return_code = subprocess.call(["afplay", audio_file]) 
