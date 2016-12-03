import hero
import urllib
import os.path
import sys
import concurrent.futures

import signal

MAX_ATTEMPTS = 3


def download_mp3(mp3, file_uri, att=0):
    if att >= MAX_ATTEMPTS:
        return

    try:
        if not os.path.isfile(file_uri):
            urllib.urlretrieve(mp3, file_uri)
    except Exception, e:
        print 'Error', e, ' ', mp3, ' Attempt n: ', att+1
        download_mp3(mp3, file_uri, att + 1)
    except:
        print 'Error'


def download(name, folder):
    for response in hero.Hero.get_heroes_responses(name):
        count = 1
        location = '{0}/{1}'.format(folder, name)

        if not os.path.exists(location):
            os.makedirs(location)

        for mp3 in response.mp3_url:
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

    executor = concurrent.futures.ProcessPoolExecutor(3)
    futures = [executor.submit(download, name, folder) for name in hero.Hero.get_heroes_names()]

    def signal_handler(signal, frame):
        for item in futures:
            item.shutdown()

    signal.signal(signal.SIGINT, signal_handler)

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    main(sys.argv[1:])
