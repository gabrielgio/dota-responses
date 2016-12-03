Z=zip
N=dota-response
T=temp


all:
	    $(Z) $(N) *.py
	    mv '$(N).zip' $(N)
			echo '#!/usr/bin/python' | cat - $(N) > $(T) && mv $(T) $(N)
			chmod +x $(N)

install:
	mv $(N) /usr/local
