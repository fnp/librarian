locale:
	find src/librarian -name '*.py' |xargs xgettext --from-code utf-8 -o - | sed '/^"POT-Creation-Date:/d' > messages.pot
	for lang in pl lt; do mkdir -p src/librarian/locale/$${lang}/LC_MESSAGES/; [ -e src/librarian/locale/$${lang}/LC_MESSAGES/messages.po ] && msgmerge -U src/librarian/locale/$${lang}/LC_MESSAGES/messages.po messages.pot || cp messages.pot src/librarian/locale/$${lang}/LC_MESSAGES/messages.po ; done
	rm messages.pot
	
