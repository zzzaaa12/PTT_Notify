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
BOARD_LIST = ['Key_Mou_Pad', 'HardwareSale', 'Gamesale']
KEYWORD_LIST = [u'鍵帽', u'鍵盤', 'PS4']
AUTHOR_LIST = ['']


class ptt_parser:
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


    def parse_ptt_board(self, board):
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

                if self.search_data(author, title):
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
                self.parse_ptt_board(board)

                if len(self.article_list):
                    mail_str = mail_str + board + ':\n'
                    print board + ':'
                for article in self.article_list:
                    mail_str = mail_str + '    ' + article['time'] + ' '  + article['author'] + ' ' + article['title'] + '\n'
                    mail_str = mail_str + '    ' + article['url'] + '\n\n'
                    print '    ' + article['time'] + ' '  + article['author'] + ' ' + article['title']
                    print '    ' + article['url'] + '\n'

            self.last_updated = datetime.now()

            if len(mail_str):
                #print 'mail content: ' + mail_str
                send_notify_mail('PTT Notify [' + self.last_updated.strftime('%m/%d %H:%M')  + ']', mail_str)
                print 'notify mail sent!!!'

            time.sleep(AUTO_UPDATE_SECS)
            os.system('clear || cls')


def main():
    parser = ptt_parser()
    parser.run()


if __name__ == '__main__':
    main()
