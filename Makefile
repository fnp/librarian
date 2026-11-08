.PHONY: build build_test test


locale:
	find src/librarian -name '*.py' |xargs xgettext --from-code utf-8 -o - | sed '/^"POT-Creation-Date:/d' > messages.pot
	for lang in pl lt; do mkdir -p src/librarian/locale/$${lang}/LC_MESSAGES/; [ -e src/librarian/locale/$${lang}/LC_MESSAGES/messages.po ] && msgmerge -U src/librarian/locale/$${lang}/LC_MESSAGES/messages.po messages.pot || cp messages.pot src/librarian/locale/$${lang}/LC_MESSAGES/messages.po ; done
	rm messages.pot


build:
	docker build -t wl/librarian:latest .

build_test:
	docker build -t wl/librarian-test:latest --target test \
		--build-arg UID=$$(id -u) --build-arg GID=$$(id -g) .

# Runs tests on the mounted working tree. Pass tox args via ARGS, e.g.:
#   make test ARGS="-e py312"
test:
	docker run --rm -v "$(CURDIR)":/src -e UV_CACHE_DIR=/src/.tox/.uv-cache \
		wl/librarian-test:latest tox $(ARGS)
