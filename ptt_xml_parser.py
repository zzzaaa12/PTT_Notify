#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import feedparser
from datetime import datetime
from send_notify import send_notify_mail

AUTO_UPDATE_SECS = 3600
BOARD_LIST = ['Key_Mou_Pad', 'HardwareSale']
KEYWORD_LIST = []
AUTHOR_LIST = []

def parse_ptt_board(board):
    now = datetime.now()
    data = feedparser.parse('http://rss.ptt.cc/' + board + '.xml')

    # board information
    board_updated_time = datetime.strptime(data['feed']['updated'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y/%m/%d %H:%M:%S')
    board_title = data['feed']['title']
    board_url = data['feed']['id']

    print 'Board: ' +  board_title + '\n' + \
          'Url: ' + board_url + '\n' + \
          'Last updated: ' + board_updated_time + '\n'

    # article infomation
    for item in data['entries']:
        article_author = item['author']
        article_title = item['title']
        article_url = item['id']
        article_publish_time = datetime.strptime(item['published'], '%Y-%m-%dT%H:%M:%SZ')

        if (now - article_publish_time).total_seconds() < AUTO_UPDATE_SECS:
            time_str = article_publish_time.strftime('%m/%d %H:%M:%S')
            print '    ' + time_str + '  ' +  article_author + ' ' + article_title + '\n' + \
                  '    ' + article_url + '\n'
    print ''


def main():
    print 'Board List: ' + str(BOARD_LIST)
    print 'Keyword:' +  str(KEYWORD_LIST)
    print 'Author: ' + str(AUTHOR_LIST) + '\n'

    for x in BOARD_LIST:
        parse_ptt_board(x)


if __name__ == '__main__':
    main()
