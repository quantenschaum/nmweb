dev:
	npm run dev

build:
	npm install
	npm run build

run:
	./nmweb.py

plugin: nmweb-plugin #build
	rm -rf $</dist
	cp -vr nmweb.py dist $<
	zip -r $<.zip $< -x "*/__*/*"


clean: nmweb-plugin
	rm -rf dist $</dist $<.zip
