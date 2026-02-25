FROM python:3.12 AS base

ARG UID=1000
ARG GID=1000

RUN     apt-get update && apt-get install -y \
	git \
	calibre \
	texlive-xetex texlive-lang-polish \
	texlive-extra-utils \
	texlive-lang-greek \
	texlive-lang-other \
	texlive-luatex \
	texlive-fonts-extra \
	texlive-fonts-extra-links \
	fonts-noto-core fonts-noto-extra


RUN addgroup --gid $GID app
RUN adduser --gid $GID --home /app --uid $UID app

USER app
ENV PATH="/app/.local/bin:$PATH"

# fonts
COPY src/librarian/fonts /app/.fonts
RUN fc-cache



FROM base AS pythons

USER root

RUN  apt-get update && apt-get install -y \
     epubcheck \
     pyenv \
     && rm -rf /var/lib/apt/lists/*

USER app

RUN pyenv install 3.11.11
RUN pyenv install 3.10.16
RUN pyenv install 3.9.21
RUN pyenv install 3.8.20

RUN pyenv global system 3.11.11 3.10.16 3.9.21 3.8.20
ENV PATH="/app/.pyenv/shims:$PATH"


FROM pythons AS test


USER app
WORKDIR /app

RUN pip install tox

COPY --chown=app:app . .

CMD ["tox"]



FROM base AS runtime

USER app
WORKDIR /app

COPY requirements.txt .
RUN pip install -i https://py.mdrn.pl/simple -r requirements.txt

COPY pyproject.toml .
COPY --chown=app:app src src
COPY scripts scripts

RUN pip install --no-cache-dir .
