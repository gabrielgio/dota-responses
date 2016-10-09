import hero
import urllib
import os.path
import sys


def main(args):

    folder = None

    if len(args) > 0:
        folder = args[0]

    if(folder is None):
        folder = 'dota2'

    print 'Welcome to Dota 2 responses!'
    if not os.path.exists(folder):
        os.makedirs(folder)

    for name in hero.Hero.get_heroes_names():
        print '====================={0}====================='.format(name)
        for response in hero.Hero.get_heroes_responses(name):
            count = 1
            location = '{0}/{1}'.format(folder, name)

            print response.text
            print '----->{0}'.format(response.cat)

            if not os.path.exists(location):
                os.makedirs(location)

            for mp3 in response.mp3_url:
                print '    {0}'.format(mp3)
                file_uri ='{0}/{1}_{2}.mp3'.format(location, response.text.strip().replace('/', ''), count)
                if not os.path.isfile(file_uri):
                    urllib.urlretrieve(mp3, file_uri)
                count += 1

if __name__ == "__main__":
    main(sys.argv[1:])
