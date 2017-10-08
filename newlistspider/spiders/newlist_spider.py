# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from newlistspider.items import NewlistItem

from scrapy.shell import inspect_response
reload(__import__('sys')).setdefaultencoding('utf-8') 
import smtplib
from datetime import datetime
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header

import requests

class NewListSpider(Spider):
	name = 'newlist'
	start_urls = ['http://www.poems.com.hk/zh-hk/product-and-service/initial-public-offerings/ipo-info/']

	def parse(self,response):
		item = NewlistItem()
		newlists = response.xpath('//table[@class="ipo-scheduled-items"]/tbody/tr')

		msg = MIMEMultipart()
		me = ("%s<"+"roy.liang@ectrend.com"+">") % (Header(u'新股认购','utf-8'),)
		msg['From']= me
		msg['To']='有心人'
		subject = u"%s 认购新港股名单" % (date.today().strftime('%Y,%m-%d'))
		if not isinstance(subject,unicode):
			subject = unicode(subject)
		msg['Subject']= subject
		msg["Accept-Language"]="zh-CN"
		msg["Accept-Charset"]="ISO-8859-1,utf-8"
		message = ''

		for newlist in newlists:
			item['code'] = newlist.xpath('./td[1]/text()').extract()[0].encode('utf8')
			item['name'] = newlist.xpath('./td[2]/a/text()').extract()[0].encode('utf8')
			item['quote'] = newlist.xpath('./td[3]/text()').extract()[0].encode('utf8')
			on_stock = ','.join(newlist.xpath('./td[4]/text()').extract())
			item['on_stock'] = datetime.strptime(on_stock.strip(),'%Y,%m-%d')
			cut_off = ','.join(newlist.xpath('./td[5]/text()').extract())
			item['cut_off'] = datetime.strptime(cut_off.strip(),'%Y,%m-%d')
			item['philip_statistic'] = newlist.xpath('./td[8]/text()').extract()[0].encode('utf8')

			if (item['cut_off'] - datetime.today()).days > 0:
				if u'億' in item['philip_statistic']:
					message += u"<div style='color:#f4424b;'>%s %s %s 认购截止 %s</div><br>\n" % (item['code'],item['name'].strip(),item['philip_statistic'].strip(),item['cut_off'].strftime('%m-%d'))
				else:
					message += u"<div>%s %s %s 认购截止 %s</div><br>\n" % (item['code'],item['name'].strip(),item['philip_statistic'].strip(),item['cut_off'].strftime('%m-%d'))
				
				with open('info.pdf', 'wb') as book:
					a = requests.get('http://research.cyberquote.com.hk/page/htm/kc/share_recommend/pdf/%s.pdf' % item['code'], stream=True)
					for block in a.iter_content(512):
						if not block:
							break
						book.write(block)

				pdfAttachment = MIMEApplication(file("info.pdf").read(),_subtype='pdf')
				pdfAttachment.add_header('content-disposition', 'attachment', filename = ('utf-8', '','%s.pdf' % item['code']))
				msg.attach(pdfAttachment)

			yield item
		if isinstance(message,unicode):
			message = str(message)
		msg.attach(MIMEText(message,'html','utf-8'))
		smtpObj = smtplib.SMTP(host='smtp.exmail.qq.com',port=587)
		smtpObj.starttls()
		smtpObj.login('roy.liang@ectrend.com','yan97624')
		smtpObj.sendmail('roy.liang@ectrend.com',['110672023@qq.com','ljcacai@163.com','lyy_1989@163.com'],msg.as_string())
		smtpObj.quit()	