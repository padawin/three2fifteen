SASS=$(shell which sass)
ifeq ($(SASS),)
$(error "sass command missing")
endif

.PHONY: css
css:
	sass web/sass/main.scss static/stylesheets/main.css

css-watch:
	sass --watch web/sass/main.scss:static/stylesheets/main.css
