#!/usr/bin/python3
# -*- coding: UTF-8 -*-

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
      msg += 'pdf: %s\n'%(self.urlpdf)
      if len(self.subjects)>0: msg+='subjects: '+' '.join(self.subjects) + '\n'
      msg += self.abstract
      return msg

