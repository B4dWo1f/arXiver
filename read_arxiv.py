#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from urllib.request import Request, urlopen
import datetime as dt
from bs4 import BeautifulSoup


def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html_doc = urlopen(req)
   html_doc = html_doc.read().decode(html_doc.headers.get_content_charset())
   return html_doc

def retrieve_url(url):
   """ Assumes url structure:  https://arxiv.org/abs/arXiv.id """
   if url[-1] == '/': url = url[:-1]
   arXiv_id = url.split('/')[-1]
   urlpdf = url.replace('/abs/','/pdf/')
   html_doc = make_request(url)
   S = BeautifulSoup(html_doc, 'html.parser')
   title = S.find('h1',class_='title mathjax').text.replace('Title:\n','')
   title = ' '.join( title.lstrip().rstrip().split() )
   for x in S.find_all('div', class_='authors'):
      x = x.text.replace('Authors:\n','')
      authors = []
      for author in x.split('\n'):
         auth = author.replace(',','').split()
         author = ' '.join(auth)
         authors.append(author)
   txt = S.find('blockquote', class_='abstract mathjax').text.lstrip().rstrip()
   txt = txt.replace('Abstract: ','')
   abstract = clean_text( txt )
   subjects = [s.text for s in S.find_all('span', class_='primary-subject') ]
   return arXiv_entry(title,authors,abstract,subjects,arXiv_id,urlpdf)

def get_paper(ID):
   return retrieve_url('https://arxiv.org/abs/%s'%(ID))

def clean_text(text):
   """ Remove dummy line breaks and double spaces """
   text = ' '.join(text.split())
   ret_text = ''
   for x in text.split('\n'):
      ret_text += x
      if x[-1] == '.': ret_text += '\n'
      else: ret_text += ' '
   return ret_text.lstrip().rstrip()


class arXiv_entry(object):
   def __init__(self,title='',authors=[],abstract='',subject=[],ID='',url=''):
      self.title = '\033[1m' + title + '\033[0m'
      self.author = authors
      self.abstract = abstract
      self.subjects = subject
      self.ID = ID
      self.url = url
   def __str__(self):
      msg =  'arXivID: %s\n'%(self.ID)
      msg += 'Title: %s\n'%(self.title)
      if len(self.subjects)>0: msg+='subjects: '+' '.join(self.subjects) + '\n'
      if self.url != '': msg += 'pdf: %s\n'%(self.url)
      msg += 'Abstract: %s'%(self.abstract)
      return msg



if __name__ == '__main__':
   url = 'https://arxiv.org/list/cond-mat/new'
   fname = 'condmat.arxiv'
   f_out = dt.datetime.now().strftime('%Y_%m_%d')+'.dat'

   html_doc = open(fname,'r').read()
   S = BeautifulSoup(html_doc, 'html.parser')
   h3 = S.find('h3').text
   date = h3.split('for')[-1].lstrip().rstrip()
   date = dt.datetime.strptime(date,'%a, %d %b %y').date()
   today = dt.datetime.now().date()
   if date != today:
      print('** Downloading')
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
         abstract = clean_text( a.text.lstrip().rstrip() )
         arXiv_id = i.text.split()[0].replace('arXiv:','')
         A = arXiv_entry(title,abstract=abstract,ID=arXiv_id,url=urlpdf)
         sections[sect].append(A)
      sect += 1


   ## Save abstracts and Score
   f = open(f_out,'a')
   for t,b in zip(titles,sections):
      print(t)
      for a in b:
         print(a)
         print('')
         resp = input("Is this paper relevant for you?\n1-Yes  2-Meh  3-Nope\n")
         if resp not in ['1','2']: resp = '3'
         f.write(a.ID+'   '+resp+'\n')
      print('\n')
   f.close()
