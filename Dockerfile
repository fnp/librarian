FROM python:3.8

ARG UID=1000
ARG GID=1000

RUN     apt-get update && apt-get install -y \
	git \
	calibre \
	texlive-xetex texlive-lang-polish


RUN addgroup --gid $GID app
RUN adduser --gid $GID --home /app --uid $UID app

RUN     apt-get install -y \
	texlive-extra-utils \
	texlive-lang-greek \
	texlive-lang-other \
	texlive-luatex \
	texlive-fonts-extra \
	texlive-fonts-extra-links \
	fonts-noto-core fonts-noto-extra



COPY dist/librarian.tar.gz /

USER app

# fonts
COPY src/librarian/fonts /app/.fonts
RUN fc-cache

RUN pip install -i https://py.mdrn.pl/simple /librarian.tar.gz


