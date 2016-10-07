import hero

if __name__ == "__main__":
    print 'Welcome to Dota 2 responses!'
    for name in hero.Hero.get_heroes_names():
        print '====================={0}====================='.format(name)
        for name in hero.Hero.get_heroes_responses(name):
            print name.text
            print '----->{0}'.format(name.cat)
            for mp3 in name.mp3_url:
                print '    {0}'.format(mp3)
