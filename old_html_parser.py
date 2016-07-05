#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
from send_notify import send_notify_mail
from HTMLParser import HTMLParser

#TODO:
#   1. Save and Clean Data
#   2. Compare Date

Target_Boards = ['Key_Mou_Pad']

class ptt_html_parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.div_ent = False
        self.all_data = ''
        self.reset_flags()

    def reset_flags(self):
        self.article = {'date':'', 'author':'', 'title':'', 'url':''}
        self.parse_author = False
        self.parse_date = False
        self.parse_title_and_url = False
        self.parse_complete = False
        self.exit_count = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs[0][1] == 'r-ent':
            self.reset_flags()
            self.div_ent = True

        if self.div_ent:
            if tag == 'a':
                self.parse_title_and_url = True
                self.article['url'] = attrs[0][1]
            elif tag == 'div' and attrs[0][1] == 'date':
                self.parse_date = True
            elif tag == 'div' and attrs[0][1] == 'author':
                self.parse_author = True

    def handle_endtag(self, tag):
        if tag == 'div' and self.parse_complete:
            self.exit_count = self.exit_count + 1
            if self.exit_count == 3:
                self.all_data = self.all_data + self.article['date'] + ' ' + self.article['author'] + ' ' + self.article['title'] + \
                                '\n      http://www.ptt.cc' +  self.article['url'] + '\n\n'

    def handle_data(self, data):
        if self.parse_title_and_url:
            self.article['title'] = data
            self.parse_title_and_url = False
        if self.parse_date:
            self.article['date'] = data
            self.parse_date = False
        if self.parse_author:
            if data == '-': # article deleted
                self.reset_flags()
                return
            self.article['author'] = data
            self.parse_author = False
            self.parse_complete = True


for board in Target_Boards:
    print '看板名稱：' + board
    print ''

    parser = ptt_html_parser()
    parser.feed(urllib.urlopen('https://www.ptt.cc/bbs/' + board + '/index.html').read())
    parser.close()

    print parser.all_data
#    send_notify_mail('PTT notify [' + board + ']', parser.all_data)
    print ''
