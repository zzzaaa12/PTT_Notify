#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import time
import feedparser
import requests
import json
from datetime import datetime
from datetime import timedelta
from send_notify import send_notify_mail

# files in this project
from setting import AUTO_UPDATE_SECS
from setting import SEND_EMAIL
from setting import BOARDS
from setting import SHOW_CONTENT
from setting import G_KEYWORDS
from setting import G_AUTHORS

class PttXmlParser:
    def __init__(self):
        self.last_updated = datetime.now() + timedelta(hours = -1)
        self.board_list = BOARDS
        for board in self.board_list:
            board['last_updated'] = datetime.now() + timedelta(hours = -1)


    def get_matches(self, board_name, title, author, content):
        for board in self.board_list:
            if board['name'].lower() != board_name.lower():
                continue

            # specific keywords
            for keyword in board['keywords']:
                if title.lower().find(keyword.lower()) > -1:
                    print 'Got (specific key words)'
                    return True

            # specific authors
            for people in board['authors']:
                if people.lower() == author.lower():
                    print 'Got (specific authors)'
                    return True

            # general keywords
            if board['search_general_keyword']:
                for keyword in G_KEYWORDS:
                    if title.lower().find(keyword.lower()) > -1:
                        print 'Got (general keywords)'
                        return True

            # general authors
            if board['search_general_author']:
                for people in G_AUTHORS:
                    if people.lower() == author.lower():
                        print 'Got (general authers)'
                        return True

            # search content
            if board['search_content']:
                for keyword in board['keywords']:
                    if content.lower().find(keyword.lower()) > -1:
                        print 'Got (specific content)'
                        return True
                if board['search_general_keyword']:
                    for keyword in board['keywords']:
                        if content.lower().find(keyword.lower()) > -1:
                            print 'Got (general content)'
                            return True

        return False


    def parse_ptt_article(self):
        for board in self.board_list:
            r_url = 'https://www.ptt.cc/atom/' + board['name'] + '.xml'
            print 'get ' + r_url
            r = requests.get(r_url, timeout=10)
            if r.status_code != 200:
                print 'get url fail!!!'
                return False

            data = feedparser.parse(r.text)

            # board information
            # 1. title: data['feed']['title']
            # 2. url: data['feed']['id']

            # article infomation
            board['article_list'] = []
            got_last_updated_time = False
            for item in data['entries']:
                author = item['author']
                title = item['title']
                url = item['id']
                content = item['content'][0]['value'].replace('<pre>', '').replace('</pre>', '')

                ## format of item['published']: 2017-04-22T08:39:34+08:00
                publish_time = datetime.strptime(item['published'], '%Y-%m-%dT%H:%M:%S+08:00')

                if (publish_time - board['last_updated']).total_seconds() > 0:
                    # parse articles and compare
                    if board['show_all_artciles'] or self.get_matches(board['name'], title, author, content):
                        article_data = {'board':'', 'author':'', 'title':'', 'url':'', 'content':''}
                        article_data['board'] = board
                        article_data['author'] = author
                        article_data['title'] = title
                        article_data['url'] = url
                        article_data['content'] = content
                        article_data['time'] = publish_time.strftime('%H:%M')
                        board['article_list'].append(article_data)

                # read the newest article and save last_updated_time from it
                if not got_last_updated_time:
                    got_last_updated_time = True
                    last_updated_time = publish_time
            board['last_updated'] = last_updated_time
        return True


    def run(self):
        while True:
            mail_str = ''
            got_board_list = ''
            print 'start at: ' + str(datetime.now().strftime('%m/%d %H:%M:%S\n'))

            try:
                self.parse_ptt_article()
            except Exception as e:
                print 'Error: An exception occurred at ' + datetime.now().strftime('%m/%d %H:%M:%S') + ': \n' + str(e) + '\n'
                time.sleep(AUTO_UPDATE_SECS)
                continue

            for board in self.board_list:
                if len(board['article_list']) == 0:
                    continue

                # create title of notify mail
                if SEND_EMAIL:
                    mail_str = mail_str + board['name'] + u'板：\n'

                    # add board name in mail title
                    if got_board_list.find(board['name']) == -1:
                        if len(got_board_list) == 0:
                            got_board_list = board['name']
                        else:
                            got_board_list = got_board_list + '/' + board['name']

                    for article in board['article_list']:
                        mail_str = mail_str + '    ' + article['time'] + '   '  + article['author'] + ' ' + article['title'] + '\n'
                        mail_str = mail_str + '    ' + article['url']
                        if SHOW_CONTENT:
                            mail_str = mail_str + '\n    ' + article['content'].replace('\n', '\n    ') + '\n'
                        mail_str = mail_str + '\n\n'

                print '\n    ' + board['name'] + u'板：'
                for article in board['article_list']:
                    print '        ' + article['time'] + ' '  + article['author'] + ' ' + article['title']
                    print '        ' + article['url']

            # save last updated time
            self.last_updated = datetime.now()
            f = open('last_updated', 'w')
            f.write(self.last_updated.strftime('%m/%d %H:%M:%S\n'))
            f.close()

            # send notity mail
            if SEND_EMAIL and len(mail_str) > 0:
                send_notify_mail('PTT [' + self.last_updated.strftime('%H:%M') + ']: ' + got_board_list, mail_str)
                print 'notify mail sent (' + self.last_updated.strftime('%m/%d %H:%M') + ')'

            print '\nfinish at ' + self.last_updated.strftime('%m/%d %H:%M:%S')
            time.sleep(AUTO_UPDATE_SECS)


def main():
    try:
        parser = PttXmlParser()
        parser.run()
    except Exception as e:
        print 'Error: An exception occurred at ' + datetime.now().strftime('%m/%d %H:%M:%S') + ': \n' + str(e) + '\n'
        if SEND_EMAIL:
            mail_str = 'An exception occurred at ' + datetime.now().strftime('%m/%d %H:%M:%S') + ':\n' + str(e) + '\n'
            send_notify_mail('Error of PTT Notify', mail_str)


if __name__ == '__main__':
    main()
