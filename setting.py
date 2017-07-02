# -*- coding: utf-8 -*-

# update interval
AUTO_UPDATE_SECS = 300

# show content in article
SHOW_CONTENT = False

# send notify mail
SEND_EMAIL = True

# general keywords and authors for all board
G_KEYWORDS = [u'程式']
G_AUTHORS = ['SYSOP', 'PTT']

# board settings
BOARDS =  [
    {
        "name": "nb-shopping",
        "authors": [],
        "keywords": ['x220'],
        "show_all_artciles": False,
        "search_general_keyword": False,
        "search_general_author": False,
        "search_content": False,
    },
    {
        "name": "Stock",
        "authors": ['chengwaye'],
        "keywords": [u'三大法人買賣'],
        "show_all_artciles": False,
        "search_general_keyword": True,
        "search_general_author": False,
        "search_content": False,
    },
    {
        "name": "HardwareSale",
        "authors": [],
        "keywords": ['SSD', u'硬碟'],
        "show_all_artciles": False,
        "search_general_keyword": False,
        "search_general_author": False,
        "search_content": False,
    },
    {
        "name": "CompBook",
        "authors": [],
        "keywords": [],
        "show_all_artciles": True,
        "search_general_keyword": False,
        "search_general_author": False,
        "search_content": False,
    }
]
