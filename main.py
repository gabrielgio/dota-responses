import hero
import urllib
import os.path

if __name__ == "__main__":
    print 'Welcome to Dota 2 responses!'
    if not os.path.exists("dota2"):
        os.makedirs("dota2")

    for name in hero.Hero.get_heroes_names():
        print '====================={0}====================='.format(name)
        for response in hero.Hero.get_heroes_responses(name):
            print response.text
            print '----->{0}'.format(response.cat)
            count = 1
            if not os.path.exists('dota2/{0}'.format(name)):
                os.makedirs('dota2/{0}'.format(name))

            for mp3 in response.mp3_url:
                print '    {0}'.format(mp3)
                urllib.urlretrieve(mp3, 'dota2/{0}/{1}_{2}.mp3'.format(name,response.text, count))
                count += 1
