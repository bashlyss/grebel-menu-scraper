NPM_BIN = node_modules/.bin/
STYLES_DIR = app/static/styles/
CSS_DIR = app/static/css/

all: styles

styles:
	@$(NPM_BIN)/node-sass -o $(CSS_DIR) $(SCSS_FLAGS) $(STYLES_DIR)

.PHONY : watch
watch: SCSS_FLAGS += -w
watch: styles

install: 
	./install.sh
