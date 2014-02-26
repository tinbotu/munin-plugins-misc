#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ts=4 sts=4 ff=unix expandtab

"""
=head1 NAME

Wildcard munin plugin to monitor price gasoline(petrol) and diesel oil in Japan by http://gogo.gs

=head1 CONFIGRATION

usage
  e.g.
  ln -s /usr/share/munin/plugins/gogogs_ /etc/munin/plugins/gogogs_13
  (13 is index of Tokyo prefecture)


Prefecture(ken) index are below::

0: 全国
1: 北海道
2: 青森県
3: 岩手県
4: 宮城県
5: 秋田県
6: 山形県
7: 福島県
8: 茨城県
9: 栃木県
10: 群馬県
11: 埼玉県
12: 千葉県
13: 東京都
14: 神奈川県
15: 新潟県
16: 富山県
17: 石川県
18: 福井県
19: 山梨県
20: 長野県
21: 岐阜県
22: 静岡県
23: 愛知県
24: 三重県
25: 滋賀県
26: 京都府
27: 大阪府
28: 兵庫県
29: 奈良県
30: 和歌山県
31: 鳥取県
32: 島根県
33: 岡山県
34: 広島県
35: 山口県
36: 徳島県
37: 香川県
38: 愛媛県
39: 高知県
40: 福岡県
41: 佐賀県
42: 長崎県
43: 熊本県
44: 大分県
45: 宮崎県
46: 鹿児島県
47: 沖縄県


=head1 MAGIC MARKERS

=head1 VERSION
Version 0.1

=head1 AUTHOR

Akira KUMAGAI <kumaguy@gmail.com>
http://github.com/tinbotu

=head1 LICENSE

GPLv2 (http://www.gnu.org/licenses/gpl-2.0.txt)

=cut

"""

import os
import sys
import re
import requests
import unittest
from xml.etree import ElementTree


class gogogs_reader(object):
    __price = {}
    __types = {u'レギュラー': 'ron89', u'ハイオク': 'ron96', u'軽油': 'diesel', u'灯油': 'kerosene', }
    __prefectures = {u'全国': 'zenkoku', u'北海道': 'hokkaido', u'青森県': 'aomori', u'岩手県': 'iwate', u'宮城県': 'miyagi', u'秋田県': 'akita', u'山形県': 'yamagata', u'福島県': 'fukushima', u'茨城県': 'ibaraki', u'栃木県': 'tochigi', u'群馬県': 'gunma', u'埼玉県': 'saitama', u'千葉県': 'chiba', u'東京都': 'tokyo', u'神奈川県': 'kanagawa', u'新潟県': 'niigata', u'富山県': 'toyama', u'石川県': 'ishikawa', u'福井県': 'fukui', u'山梨県': 'yamanashi', u'長野県': 'nagano', u'岐阜県': 'gifu', u'静岡県': 'shizuoka', u'愛知県': 'aichi', u'三重県': 'mie', u'滋賀県': 'shiga', u'京都府': 'kyoto', u'大阪府': 'osaka', u'兵庫県': 'hyogo', u'奈良県': 'nara', u'和歌山県': 'wakayama', u'鳥取県': 'tottori', u'島根県': 'shimane', u'岡山県': 'okayama', u'広島県': 'hiroshima', u'山口県': 'yamaguchi', u'徳島県': 'tokushima', u'香川県': 'kagawa', u'愛媛県': 'ehime', u'高知県': 'kochi', u'福岡県': 'fukuoka', u'佐賀県': 'saga', u'長崎県': 'nagasaki', u'熊本県': 'kumamoto', u'大分県': 'oita', u'宮崎県': 'miyazaki', u'鹿児島県': 'kagoshima', u'沖縄県': 'okinawa'}

    def __init__(self):
        self.__apiurl = "http://api.gogo.gs/parts/xml/%d.xml"
        self.clear()

    def clear(self):
        self.__price = {}

    def fetch(self, prefindex=13, m=10, d=21, h=22):
        payload = {"m": m, "d": d, "h": h}
        url = self.__apiurl % prefindex
        r = requests.get(url, params=payload)

        if not r.status_code == requests.codes.ok:
            return False

        xmlroot = ElementTree.fromstring(r.content)

        areaname = xmlroot.find("AreaName").text
        for ken_j, ken_e in self.__prefectures.iteritems():
            if areaname == ken_j:
                self.__price["area"] = ken_e
                break

        for n in xmlroot.find("Data").iter("Item"):
            for k, v in self.__types.iteritems():
                if n.find("Type").text == k:
                    if v == "kerosene":  # kerosene unit is 一斗
                        self.__price[v] = round(float(n.find("Price").text)/18.0, 1)
                    else:
                        self.__price[v] = float(n.find("Price").text)

        return self.__price


class Testgogogsreader(unittest.TestCase):
    pass


def munin_config(area="", draw=[]):
    gastypes = ["ron96", "ron89", "diesel", "kerosene"]
    print "graph_title GasolinePrice", area
    print "graph_args -u 180"
    print "graph_scale no"
    print "graph_order ron89 ron96 diesel kerosene"
    print "graph_vlabel JPY"
    print "graph_info GasolinePriceAverage", area

    print "ron89.colour D10000"
    print "ron96.colour CFCF00"
    print "diesel.colour 00AA00"
    print "kerosene.colour 0000AA"

    print "ron89.label RON89"
    print "ron96.label RON96"
    print "diesel.label Diesel"
    print "kerosene.label Kerosene"

    for name in gastypes:
        print "%s.type GAUGE" % name
        print "%s.draw LINE2" % name
        if not name in draw:
            print "%s.graph no" % name


def main():
    argc = len(sys.argv)
    myfilename = list(os.path.split(sys.argv[0]))[1]

    match_prefnum = re.search(r'_([0-9]+)$', myfilename)
    match_gastype = re.search(r'_([rpdk]+)_', myfilename)

    prefnum = 0
    if match_prefnum:
        prefnum = int(match_prefnum.group(1))

    draw_gastype = ["ron89", "ron96", "diesel", "kerosene", ]
    if match_gastype:
        draw_gastype = []
        if match_gastype.group(1).count("r") > 0: draw_gastype.append("ron89")
        if match_gastype.group(1).count("p") > 0: draw_gastype.append("ron96")
        if match_gastype.group(1).count("d") > 0: draw_gastype.append("diesel")
        if match_gastype.group(1).count("k") > 0: draw_gastype.append("kerosene")

    g = gogogs_reader()
    p = g.fetch(prefindex=prefnum)

    if argc == 2:
        param = sys.argv[1]
        if param == "config":
            p = g.fetch(prefindex=prefnum)
            munin_config(area=p.get("area"), draw=draw_gastype)
            sys.exit(0)
        elif param == "autoconf" or param == "suggest":
            print "No"
            sys.exit(0)

    for k, v in p.iteritems():
        print "%s.value %s" % (k, v)


if __name__ == "__main__":
    main()
