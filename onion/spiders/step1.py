# -*- coding: utf-8 -*-
from scrapy import Request 
from scrapy.spiders import Spider
from onion.items import OnionItem
import random
import subprocess
all_headers={'Host': 'pjaopjqvjk6be4wz.onion',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'}
all_cookies=[{'MARKET_SESSION':'jq0n0mum0sp62477aovie02ag1'},{'MARKET_SESSION':'2fsa616dlvu7mjdrfdqovtpeu6'},
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
  ] # for multiple sessions

class BackupSpider(Spider):
    name = 'step1'
    def start_requests(self):
        yield Request(url='http://pjaopjqvjk6be4wz.onion/?page=1', 
        headers=all_headers,
        cookies=random.choice(all_cookies))
  #Main parse, extract item list of a page
    #def start_requests(self):
    #    return [scrapy.Request(url='http://4buzlb3uhrjby2sb.onion/?category=104', cookies={'MARKET_SESSION':'r2igr631d2vcd5ie1itgrnaik7'})]
    def parse(self, response):
        captcha = response.xpath('//div[@class="ddos"]/text()').extract()
        #detect captcha and solve it in browser
        if captcha:
           audio_file = "/Users/Sean/Downloads/cartoon002.wav" 
           return_code = subprocess.call(["afplay", audio_file]) 
           captcha_solution = input('又双叒叕要输入验证码了！')
           print("登录中")
           yield Request(url = response.url, cookies=random.choice(all_cookies), headers=all_headers, callback=self.parse, dont_filter= True)
        else:
           item = OnionItem()
           entries = response.xpath('.//div[@class="around"]')
           for entry in entries:
              item['item_name'] = entry.xpath('.//div[@class="text oTitle"]/a/text()').extract()[0].strip()
              item['item_link'] = entry.xpath('.//div[@class="text oTitle"]/a/@href').extract()[0].strip()
              item['item_price'] = entry.xpath('.//div[@class="bottom oPrice"]/text()').extract()[0].strip()
              item['item_seller'] = entry.xpath('.//div[@class="oVendor"]/a[1]/text()').extract()[0].strip()
              item['item_delivery'] = entry.xpath('.//div[@class="oShips"]/span/text()').extract()[0].strip()
              item['item_sales'] = ''
              item['item_category'] = ''
              ipage_url = 'http://4buzlb3uhrjby2sb.onion/' + item['item_link'].lstrip('.')
              yield item

        next_url = response.xpath('//a[@class="gPager lastPager"]/@href').extract()
        if len(next_url) != 0:
           next_full_url = 'http://pjaopjqvjk6be4wz.onion/' + next_url[0]
           yield Request(url=next_full_url, cookies = random.choice(all_cookies))

      