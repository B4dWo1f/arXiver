#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from urllib.request import Request, urlopen
import datetime as dt
from bs4 import BeautifulSoup


def make_request(url):
   """
     Make http request
   """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html_doc = urlopen(req)
   html_doc = html_doc.read().decode(html_doc.headers.get_content_charset())
   return html_doc

class arXiv_entry(object):
   def __init__(self,title='',authors=[],abstract='',subject=[],ID='',url=''):
      self.title = title
      self.author = authors
      self.abstract = abstract
      self.subjects = subject
      self.ID = ID
      self.url = url
   def __str__(self):
      msg =  'arXivID: %s\n'%(self.ID)
      msg += 'Title: %s\n'%(self.title)
      msg += 'Abstract: %s'%(self.abstract)
      if self.url != '': msg += '\npdf: %s'%(self.url)
      return msg


url = 'https://arxiv.org/list/cond-mat/new'
fname = 'condmat.arxiv'


html_doc = open(fname,'r').read()
S = BeautifulSoup(html_doc, 'html.parser')
h3 = S.find('h3').text
date = h3.split('for')[-1].lstrip().rstrip()
date = dt.datetime.strptime(date,'%a, %d %b %y').date()
today = dt.datetime.now().date()
if date != today:
   html_doc = make_request(url) # Main web site
   f = open(fname,'w')
   f.write(html_doc)
   f.close()


S = BeautifulSoup(html_doc, 'html.parser')


NewSub = []
CrossList = []
Replacements = []
sections = [NewSub, CrossList, Replacements]
titles = []
sect = 0
for dl,h3 in zip(S.find_all('dl'),S.find_all('h3')):
   h = '** ' + h3.text + ' *'
   while len(h) < 80:
      h = h + '*'
   titles.append(h)
   for i,u,t,a in zip(dl.find_all('span',class_='list-identifier'),\
                      dl.find_all('span',class_='list-identifier'),\
                      dl.find_all('div', class_='list-title mathjax'),\
                      dl.find_all('p', class_='mathjax')):
      for p in u.find_all('a',href=True):
         if p.get('title') == 'Download PDF':
            urlpdf = 'http://arxiv.org'+p.get('href')
      title = t.text.replace('Title: ','').lstrip().rstrip()
      abstract = a.text.lstrip().rstrip()
      arXiv_id = i.text.split()[0].replace('arXiv:','')
      A = arXiv_entry(title,abstract=abstract,ID=arXiv_id,url=urlpdf)
      sections[sect].append(A)
   sect += 1

for t,b in zip(titles,sections):
   print(t)
   for a in b:
      print(a)
      print('')
   print('')
