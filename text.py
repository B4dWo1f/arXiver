#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import console

def clean(text):
   """ Remove dummy line breaks and double spaces """
   text = ' '.join(text.split())
   ret_text = ''
   for x in text.split('\n'):
      ret_text += x
      if x[-1] == '.': ret_text += '\n'
      else: ret_text += ' '
   return ret_text.lstrip().rstrip()

def justifyRL(str1,str2,w=0):
   """
     Align string 1 and 2 to the left and right respectively.
     If no width is given, use the width of the console
   """
   if str2 == '': return str1
   if w == 0: X,Y = console.getTerminalSize()
   else: X = w
   total = str1+str2
   while len(total) < X:
      str1 = str1 + ' '
      total = str1+str2
   return total

def center(string):
   """ Center text in the console width """
   X,Y = console.getTerminalSize()
   rest = X - len(string)
   if rest > 0:
      padd = rest//2
      return ' '*padd + string
   else: return string

def title(text):
   """ Pretty print for titles """
   X,Y = console.getTerminalSize()
   msg = '='*X + '\n'
   msg += '\033[1m' +center(text)+ '\033[0m'+'\n'
   msg += '='*X
   return msg
