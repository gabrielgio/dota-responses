from HTMLParser import HTMLParser
import requests

base_url = 'http://dota2.gamepedia.com/'


class HeroResponse(object):

    def __init__(self):
        self.text = ''
        self.mp3_url = []
        self.cat = ''


class HeroMp3Response(HTMLParser):

    def __init__(self):
        self.mlist = []
        self.valid_a = False
        self.li = False
        self.cat = ''
        self.valid_span = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.li = True
            r = HeroResponse()
            self.mlist.append(r)

        if tag == 'span':
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == 'mw-headline':
                        self.valid_span = True;

        if tag == 'a':
            if len(attrs) > 0:
                href = ''
                title = False

                if self.li:
                   for attr in attrs:
                        if attr[0] == 'href':
                            href = attr[1]
                        if attr[0] == 'title':
                            title = attr[1] == 'Play'

                if title:
                    self.valid_a = True
                    self.mlist[-1].mp3_url.append(href)


    def handle_data(self, data):
        if self.li and self.valid_a:
            self.mlist[-1].text = data
            self.mlist[-1].cat = self.cat

        if self.valid_span:
            self.cat = data;

    def handle_endtag(self, tag):
        if tag == 'li':
            self.li = False
            self.valid_a = False

        if tag == 'span':
            self.valid_span = False


class HeroNamesParser(HTMLParser):

    alist = []

    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            if len(attrs) > 0:
                w = False
                h = False
                png = ''
                for attr in attrs:
                    if attr[0] == 'width' and attr[1] == '178':
                        w = True
                    if attr[0] == 'height' and attr[1] == '100':
                        h = True

                    if attr[0] == 'alt':
                        png = attr[1]

                if w and h:
                    self.alist.append(png.replace(' ', '_')
                                      .replace('.png','')
                                      .replace('\'','%27'))

class Hero(object):

    @staticmethod
    def get_heroes_responses(name):
        url = '{0}{1}/Responses'.format(base_url,name)
        r = requests.get(url)
        pure_html = r.content
        parser = HeroMp3Response()
        parser.feed(pure_html)
        return  [item for item in parser.mlist if item.text]

    @staticmethod
    def get_heroes_names():
        url = '{0}heroes'.format(base_url)
        r = requests.get(url)
        pure_html = r.content
        parser = HeroNamesParser()
        parser.feed(pure_html)
        return parser.alist;