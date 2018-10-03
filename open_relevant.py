#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import datetime as dt

now = dt.datetime.now()
today = now.date().strftime('%Y_%m_%d')
relevants = os.popen('grep -v " 3" %s.dat'%(today)).read()
relevants = relevants.splitlines()

base_url = 'https://arxiv.org/pdf/'
urls = []
for i in relevants:
   arxivID = i.split()[0]
   urls.append(base_url+arxivID)

com = 'firefox -new-tab -url ' + ' -new-tab -url '.join(urls)
print(com)
os.system('nohup ' + com + ' &')
