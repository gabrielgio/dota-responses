from HTMLParser import HTMLParser
import requests

base_url = 'http://dota2.gamepedia.com/'


class HeroResponse(object):

    def __init__(self):
        self.text = ''
        self.mp3_url = []
        self.cat = ''


class _HeroMp3Parser(HTMLParser):

    mp3_list = []
    __valid_a = False
    __li = False
    __cat = ''
    __valid_span = False

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.__li = True
            r = HeroResponse()
            self.mp3_list.append(r)

        if tag == 'span':
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == 'mw-headline':
                        self.__valid_span = True;

        if tag == 'a':
            if len(attrs) > 0:
                href = ''
                title = False

                if self.__li:
                   for attr in attrs:
                        if attr[0] == 'href':
                            href = attr[1]
                        if attr[0] == 'title':
                            title = attr[1] == 'Play'

                if title:
                    self.__valid_a = True
                    self.mp3_list[-1].mp3_url.append(href)


    def handle_data(self, data):
        if self.__li and self.__valid_a:
            self.mp3_list[-1].text = data
            self.mp3_list[-1].cat = self.__cat

        if self.__valid_span:
            self.__cat = data;

    def handle_endtag(self, tag):
        if tag == 'li':
            self.__li = False
            self.__valid_a = False

        if tag == 'span':
            self.__valid_span = False


class _HeroNamesParser(HTMLParser):

    name_list = []

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
                    self.name_list.append(png.replace(' ', '_')
                                          .replace('.png','')
                                          .replace('\'','%27'))

class Hero(object):

    @staticmethod
    def get_heroes_responses(name):
        url = '{0}{1}/Responses'.format(base_url,name)
        r = requests.get(url)
        pure_html = r.content
        parser = _HeroMp3Parser()
        parser.feed(pure_html)
        return [item for item in parser.mp3_list if item.text]

    @staticmethod
    def get_heroes_names():
        url = '{0}heroes'.format(base_url)
        r = requests.get(url)
        pure_html = r.content
        parser = _HeroNamesParser()
        parser.feed(pure_html)
        return parser.name_list;