#!/usr/bin/python3
# -*- coding: UTF-8 -*-


from urllib.request import Request, urlopen
import datetime as dt
from bs4 import BeautifulSoup
import text
from arxiv import arXiv_entry, author


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
   abstract = text.clean( txt )
   subjects = [s.text for s in S.find_all('span', class_='primary-subject') ]
   return arXiv_entry(title,authors,abstract,subjects,arXiv_id,urlpdf)

def get_paper(ID):
   return retrieve_url('https://arxiv.org/abs/%s'%(ID))

#def clean_text(text):
#   """ Remove dummy line breaks and double spaces """
#   text = ' '.join(text.split())
#   ret_text = ''
#   for x in text.split('\n'):
#      ret_text += x
#      if x[-1] == '.': ret_text += '\n'
#      else: ret_text += ' '
#   return ret_text.lstrip().rstrip()


#class arXiv_entry(object):
#   def __init__(self,title='',authors=[],abstract='',subject=[],ID='',url=''):
#      self.title = '\033[1m' + title + '\033[0m'
#      self.author = authors
#      self.abstract = abstract
#      self.subjects = subject
#      self.ID = ID
#      self.url = url
#   def __str__(self):
#      msg =  'arXivID: %s\n'%(self.ID)
#      msg += 'Title: %s\n'%(self.title)
#      if len(self.subjects)>0: msg+='subjects: '+' '.join(self.subjects) + '\n'
#      if self.url != '': msg += 'pdf: %s\n'%(self.url)
#      msg += 'Abstract: %s'%(self.abstract)
#      return msg



if __name__ == '__main__':
   url = 'https://arxiv.org/list/cond-mat/new'
   URLbase = 'https://arxiv.org'
   fname = 'condmat.arxiv'
   today = dt.datetime.now().date()
   f_out = today.strftime('%Y_%m_%d')+'.dat'

   try:
      html_doc = open(fname,'r').read()
      S = BeautifulSoup(html_doc, 'html.parser')
      h3 = S.find('h3').text
      date = h3.split('for')[-1].lstrip().rstrip()
      date = dt.datetime.strptime(date,'%a, %d %b %y').date()
   except FileNotFoundError: date = today - dt.timedelta(days=5)

   if date != today:
      print('** Downloading')
      html_doc = make_request(url) # Main web site
      f = open(fname,'w')
      f.write(html_doc)
      f.close()
   else: print('** NOT downloading')


   S = BeautifulSoup(html_doc, 'html.parser')


   NewSub = []
   CrossList = []
   Replacements = []
   sections = [NewSub, CrossList, Replacements]
   titles = []
   sect = 0
   for dl,h3 in zip(S.find_all('dl'),S.find_all('h3')):
      ## Skip replacements
      section = h3.text.split('for')[0].lstrip().rstrip() 
      if section not in ['New submissions', 'Cross-lists']: continue
      ## report section.  #TODO log this
      h = '** ' + h3.text + ' *'
      while len(h) < 80:
         h = h + '*'
      titles.append(h)
      for dt_tag,dd_tag in zip(dl.find_all('dt'),\
                               dl.find_all('dd')):
         ## parsing dt tag
         index = int(dt_tag.find('a').text.replace('[','').replace(']',''))
         arxivID = dt_tag.find('a',title='Abstract').text.replace('arXiv:','')
         URLabs = URLbase + dt_tag.find('a',title='Abstract')['href']
         URLpdf = URLbase + dt_tag.find('a',title='Download PDF')['href']
         ## parsing dd tag
         # Title
         title = dd_tag.find('div',class_='list-title mathjax').text
         title = text.clean(title.replace('Title: ',''))
         # Authors
         authors = []
         for auth in dd_tag.find('div',class_='list-authors').find_all('a'):
            authors.append( author(auth.text,URLbase+auth['href']) )
         # Subjects
         subjects = dd_tag.find('div',class_='list-subjects').text
         subjects = subjects.replace('Subjects: ','').split(';')
         subjects = [x.lstrip().rstrip() for x in subjects]
         # Abstract
         abstract = text.clean(dd_tag.find('p', class_='mathjax').text)
         ## arXiv entry
         A = arXiv_entry(title=title, authors=authors, abstract=abstract,
                         subject=subjects, ID=arxivID, urlabs=URLabs,
                         urlpdf=URLpdf, index=index)

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
         print('')
      print('\n')
   f.close()
