#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import read_arxiv as arXiv
from random import choice

url = choice(['1809.06863', '1809.06884', '1809.06886', '1809.06889',
              '1809.06892', '1809.06919', '1809.06922', '1809.06930',
              '1809.06938', '1809.06939', '1809.06971'])
A = arXiv.get_paper(url)

print(A)
