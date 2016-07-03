#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import urllib
import requests
import xml.etree.ElementTree as ET
from send_notify import send_notify_mail

Target_Boards = ['Key_Mou_Pad']

xml_data = requests.get('http://rss.ptt.cc/Key_Mou_Pad.xml').content
fp = open('data.xml', 'w')
fp.write(xml_data);
fp.close()

tree = ET.parse('data.xml')
root = tree.getroot()

for neighbor in root.iter('name'):
    print neighbor.attrib
