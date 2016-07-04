#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import feedparser
from send_notify import send_notify_mail

Target_Boards = ['Key_Mou_Pad']

data = feedparser.parse('http://rss.ptt.cc/Key_Mou_Pad.xml')
print 'Board: ' +  data['feed']['title'] + '\n' + \
      'Url: ' + data['feed']['id'] + '\n' + \
      'Last updated:' + data['feed']['updated'] + '\n'

for item in data['entries']:
    print item['published'] + ' ' + item['id'] + '\n' + \
          item['author'] + ' ' + item['title'] + '\n'

