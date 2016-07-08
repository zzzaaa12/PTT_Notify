#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import feedparser
from datetime import datetime
from datetime import timedelta
from send_notify import send_notify_mail

AUTO_UPDATE_SECS = 300
BOARD_LIST = ['Key_Mou_Pad', 'HardwareSale', 'DC_SALE', 'CompBook']
SHOW_ALL_BOARD = ['HardwareSale']
KEYWORD_LIST = [u'鍵帽', u'鍵盤']
AUTHOR_LIST = ['']

class PttXmlParser:
    def __init__(self):
        self.last_updated = datetime.now() + timedelta(hours = -1)

    def search_data(self, author, title):
        for x in AUTHOR_LIST:
            if author == x:
                return True
        for x in KEYWORD_LIST:
            if title.lower().find(x.lower()) != -1:
                return True
        return False


    def parse_ptt_board(self, board, show_all):
        now = datetime.now()
        data = feedparser.parse('http://rss.ptt.cc/' + board + '.xml')

        # board information
        board_updated_time = datetime.strptime(data['feed']['updated'], '%Y-%m-%dT%H:%M:%SZ')
        board_title = data['feed']['title']
        board_url = data['feed']['id']

        # article infomation
        self.article_list = []
        for item in data['entries']:
            author = item['author']
            title = item['title']
            url = item['id']
            publish_time = datetime.strptime(item['published'], '%Y-%m-%dT%H:%M:%SZ')

            if (publish_time - self.last_updated).total_seconds() > 0:
                time_str = publish_time.strftime('%m/%d %H:%M:%S')
                if show_all or self.search_data(author, title):
                    article_data = {'board':'', 'author':'', 'title':'', 'url':''} 
                    article_data['board'] = board
                    article_data['author'] = author
                    article_data['title'] = title
                    article_data['url'] = url
                    article_data['time'] = time_str
                    self.article_list.append(article_data)


    def print_list_info(self):
        keyword_str = ''
        for i in range(len(KEYWORD_LIST)):
            if i > 0:
                keyword_str = keyword_str + ', ' + "'" + KEYWORD_LIST[i] + "'"
            elif i == 0:
                keyword_str = "'" + KEYWORD_LIST[i] + "'"

        print 'Board List: ' + str(BOARD_LIST)
        print 'Keyword List: ' + '[' + keyword_str + ']'
        print 'Author List: ' + str(AUTHOR_LIST)


    def run(self):
        self.print_list_info()

        while True:
            mail_str = ''
            for board in BOARD_LIST:

                # check show all article or not
                show_all = False
                for x in SHOW_ALL_BOARD:
                    if str(x) == str(board):
                        show_all = True

                self.parse_ptt_board(board, show_all)

                if len(self.article_list):
                    mail_str = mail_str + board + ':\n'
                    print board + ':'
                for article in self.article_list:
                    mail_str = mail_str + '    ' + article['time'] + ' '  + article['author'] + ' ' + article['title'] + '\n'
                    mail_str = mail_str + '    ' + article['url'] + '\n\n'
                    print '    ' + article['time'] + ' '  + article['author'] + ' ' + article['title']
                    print '    ' + article['url'] + '\n'

            self.last_updated = datetime.now()
            f = open('last_updated', 'w')
            f.write(self.last_updated.strftime('%m/%d %H:%M:%S\n'))
            f.close()

            if len(mail_str):
#                print 'mail content: ' + mail_str
                send_notify_mail('PTT new article [' + self.last_updated.strftime('%m/%d %H:%M') + ']', mail_str)
                print 'notify mail sent (' + self.last_updated.strftime('%m/%d %H:%M') + ')'

            print 'updated at ' + self.last_updated.strftime('%m/%d %H:%M:%S')
            time.sleep(AUTO_UPDATE_SECS)
#            os.system('clear || cls')


def main():
    parser = PttXmlParser()
    parser.run()


if __name__ == '__main__':
    main()
