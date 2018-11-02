#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from urllib.request import Request, urlopen
import text


class author(object):
   def __init__(self,name='',href=''):
      self.name = name
      self.url = href
   def __str__(self):
      msg = self.name + '\n'
      if len(self.url) > 0: msg += self.url + '\n'
      return msg

class arXiv_entry(object):
   def __init__(self,title='', authors=[], abstract='', subject=[], ID='',\
                     urlabs='', urlpdf='', index=None):
      #self.title = '\033[1m' + title + '\033[0m'
      self.title = title
      self.author = authors
      self.abstract = abstract
      self.subjects = subject
      self.ID = ID
      self.urlabs = urlabs
      self.urlpdf = urlpdf
      self.index = index
   def __str__(self):
      #msg = '\033[1m' + text.center('%s\n'%(self.title)) + '\033[0m'
      msg = ''
      if self.index != None: msg += '[%s] '%(self.index)
      msg +=  'arXivID: %s\n'%(self.ID)
      msg += text.title(self.title)
      msg += 'Author'
      if len(self.author) > 1: msg += 's: '
      else: msg += ': '
      msg += ', '.join([a.name for a in self.author]) + '\n'
      msg += self.abstract+'\n'
      if len(self.subjects)>0: msg+='subjects: '+' '.join(self.subjects) + '\n'
      msg += 'pdf: %s'%(self.urlpdf)
      return msg

def make_request(url):
   """ Make http request """
   req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
   html_doc = urlopen(req)
   html_doc = html_doc.read().decode(html_doc.headers.get_content_charset())
   return html_doc

def get_paper_info(url):
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

if __name__ == '__main__':
   url = 'https://arxiv.org/list/cond-mat/new'
   URLbase = 'https://arxiv.org'
   html_doc = make_request(url) # Main web site
   fname = here + '/data/' + today.strftime('%y%m.%d') + '.arxiv'
   
   f = open(fname,'w')
   f.write(html_doc)
   f.close()
