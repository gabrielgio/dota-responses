N=dota-response


all:
	    nuitka --recurse-on --recurse-directory --remove-output --portable --python-version=2.7 __main__.py
	    mv __main__.exe $(N)
	    rm -rf __main__.build  __main__.dist

install:
	mv $(N) /usr/local
