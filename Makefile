locale:
	find src/librarian -name '*.py' |xargs xgettext --from-code utf-8 -o - | sed '/^"POT-Creation-Date:/d' > messages.pot
	for lang in pl; do msgmerge -U src/librarian/locale/$${lang}/LC_MESSAGES/messages.po messages.pot; done
	rm messages.pot
	
