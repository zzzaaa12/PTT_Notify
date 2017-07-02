#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import feedparser
import requests
from datetime import datetime
from datetime import timedelta
from send_notify import send_notify_mail

# files in this project
from setting import AUTO_UPDATE_SECS
from setting import BOARD_LIST
from setting import SHOW_ALL_BOARD
from setting import KEYWORD_LIST
from setting import AUTHOR_LIST

class PttXmlParser:
    def __init__(self):
        self.last_updated = datetime.now() + timedelta(hours = -1)
        self.board_list = BOARD_LIST
        self.board_data = []
        for x in SHOW_ALL_BOARD:
            if x not in self.board_list:
                self.board_list.append(x)

    def prepare_board_info(self):
        for x in self.board_list:
            # get ptt articles in the last hour at first run
            data = {'board':'', 'last_updated': datetime.now() + timedelta(hours = -1)}
            data['board'] = x
            self.board_data.append(data)

    def search_data(self, author, title):
        for x in AUTHOR_LIST:
            if author == x:
                return True
        for x in KEYWORD_LIST:
            if title.lower().find(x.lower()) != -1:
                return True
        return False


    def parse_ptt_article(self, board, show_all):
        got_last_updated_time = False
        now = datetime.now()

        r = requests.get('https://www.ptt.cc/atom/' + board + '.xml')
        if r.status_code != 200:
            return False

        data = feedparser.parse(r.text)

        # board information
        board_title = data['feed']['title']
        board_url = data['feed']['id']

        for x in self.board_data:
            if board == x['board']:
                board_last_updated = x['last_updated']
                break

        # article infomation
        self.article_list = []
        for item in data['entries']:
            author = item['author']
            title = item['title']
            url = item['id']

            ## format of item['published']: 2017-04-22T08:39:34+08:00
            publish_time = datetime.strptime(item['published'], '%Y-%m-%dT%H:%M:%S+08:00')

            # get and save last_updated_time
            if not got_last_updated_time:
                last_article_time = publish_time
                got_last_updated_time = True
                x['last_updated'] = last_article_time

            if (publish_time - board_last_updated).total_seconds() > 0:
                # parse articles and compare
                if show_all or self.search_data(author, title):
                    article_data = {'board':'', 'author':'', 'title':'', 'url':''} 
                    article_data['board'] = board
                    article_data['author'] = author
                    article_data['title'] = title
                    article_data['url'] = url
                    article_data['time'] = publish_time.strftime('%H:%M')
                    self.article_list.append(article_data)

        return True


    def print_list_info(self):
        keyword_str = ''
        for i in range(len(KEYWORD_LIST)):
            if i > 0:
                keyword_str = keyword_str + ', ' + "'" + KEYWORD_LIST[i] + "'"
            elif i == 0:
                keyword_str = "'" + KEYWORD_LIST[i] + "'"

        print 'Board List (show all): ' + str(SHOW_ALL_BOARD)
        print 'Board List: ' + str(self.board_list)
        print 'Keyword List: ' + '[' + keyword_str + ']'
        print 'Author List: ' + str(AUTHOR_LIST)


    def run(self):
        self.print_list_info()
        self.prepare_board_info()

        while True:
            mail_str = ''
            got_board_list = ''
            for board in self.board_list:

                # check show all article or not
                show_all = False
                for x in SHOW_ALL_BOARD:
                    if str(x) == str(board):
                        show_all = True
                        break

                # parse title of article
                try:
                    if not self.parse_ptt_article(board, show_all):
                        print 'Error: Cannot get articles in board "' + board + '"'
                except Exception as e:
                    print e
                    print '\tError: An exception occurred at ' + datetime.now().strftime('%m/%d %H:%M:%S')
                    break

                # check the articles that be selected
                if len(self.article_list) == 0:
                    continue

                # create title of notify mail
                mail_str = mail_str + board + u'板：\n'
                if got_board_list.find(board) == -1:
                    if len(got_board_list) == 0:
                        got_board_list = board
                    else:
                        got_board_list = got_board_list + '/' + board
                print '    ' + board + u'板：'

                # create content of notify mail
                for article in self.article_list:
                    mail_str = mail_str + '    ' + article['time'] + '   '  + article['author'] + ' ' + article['title'] + '\n'
                    mail_str = mail_str + '    ' + article['url'] + '\n\n'
                    print '        ' + article['time'] + ' '  + article['author'] + ' ' + article['title']
                    print '        ' + article['url'] + '\n'

            # save last updated time
            self.last_updated = datetime.now()
            f = open('last_updated', 'w')
            f.write(self.last_updated.strftime('%m/%d %H:%M:%S\n'))
            f.close()

            # send notity mail
            if len(mail_str) > 0:
                send_notify_mail('PTT [' + self.last_updated.strftime('%H:%M') + ']: ' + got_board_list, mail_str)
                print 'notify mail sent (' + self.last_updated.strftime('%m/%d %H:%M') + ')'

            print 'updated at ' + self.last_updated.strftime('%m/%d %H:%M:%S')
            time.sleep(AUTO_UPDATE_SECS)


def main():
    parser = PttXmlParser()
    parser.run()


if __name__ == '__main__':
    main()
