import urllib
import os.path
from urlparse import urlparse
import sys, httplib
import signal
from HTMLParser import HTMLParser
from joblib import Parallel, delayed
from multiprocessing import Process, Manager

BASE_URL = 'http://dota2.gamepedia.com/'

manager = Manager()
flags = manager.dict({'stop': False})


class HeroResponse(object):
    def __init__(self):
        self.text = ''
        self.mp3_url = []
        self.cat = ''


class _HeroMp3Parser(HTMLParser):
    def __init__(self):
        self.mp3_list = []
        self.__valid_a = False
        self.__li = False
        self.__cat = ''
        self.__valid_span = False
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.__li = True
            r = HeroResponse()
            self.mp3_list.append(r)

        if tag == 'span':
            for attr in attrs:
                if attr[0] == 'class':
                    if attr[1] == 'mw-headline':
                        self.__valid_span = True

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
            self.__cat = data

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
                                          .replace('.png', '')
                                          .replace('\'', '%27'))


class Hero(object):
    @staticmethod
    def get_heroes_responses(name):
        url = '{0}{1}/Responses'.format(BASE_URL, name)
        url = urlparse(url)
        conn = httplib.HTTPConnection(url.netloc)
        conn.request("GET", url.path)
        res = conn.getresponse()
        pure_html = res.read()
        parser = _HeroMp3Parser()
        parser.feed(pure_html)
        return [item for item in parser.mp3_list if item.text]

    @staticmethod
    def get_heroes_names():
        url = '{0}Heroes'.format(BASE_URL)
        url = urlparse(url)
        conn = httplib.HTTPConnection(url.netloc)
        conn.request("GET", url.path)
        res = conn.getresponse()
        pure_html = res.read()
        parser = _HeroNamesParser()
        parser.feed(pure_html)
        return parser.name_list


def download_mp3(mp3, file_uri):
    try:
        if not os.path.isfile(file_uri):
            urllib.urlretrieve(mp3, file_uri)
    except Exception, e:
        print 'Error', e, ' ', mp3
        download_mp3(mp3, file_uri)
    except:
        print 'Error'


def download(name, folder):
    for response in Hero.get_heroes_responses(name):
        if flags['stop']:
            break
        count = 1
        location = '{0}/{1}'.format(folder, name)

        if not os.path.exists(location):
            os.makedirs(location)

        for mp3 in response.mp3_url:
            if flags['stop']:
                break
            file_uri = '{0}/{1}_{2}.mp3'.format(location, response.text.strip().replace('/', ''), count)
            download_mp3(mp3, file_uri)
            count += 1


def main(args):
    folder = None

    if len(args) > 0:
        folder = args[0]

    if folder is None:
        folder = 'dota2'

    print 'Downloading'

    if not os.path.exists(folder):
        os.makedirs(folder)

    def signal_handler(signal, frame):
        flags['stop'] = True;

    signal.signal(signal.SIGINT, signal_handler)

    item = Parallel(n_jobs=8)(delayed(download)(name, folder) for name in Hero.get_heroes_names())
    print item


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print '\nSee you!'
