THEME_DIR ?= ../oink
.PHONY: serve build clean check

HUGO ?= hugo

serve:
	$(HUGO) server --buildDrafts --disableFastRender

build:
	$(HUGO) --cleanDestinationDir --gc --minify --environment production \
		--printPathWarnings

clean:
	rm -rf public resources

check: build
	python3 scripts/check_site.py

.PHONY: dev
dev:
	GOWORK=off HUGO_MODULE_WORKSPACE=off HUGO_MODULE_REPLACEMENTS='github.com/pgsty/oink -> $(abspath $(THEME_DIR))' $(HUGO) server --bind 127.0.0.1 --renderToMemory
