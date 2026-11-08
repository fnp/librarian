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



FROM base AS test

USER root

RUN  apt-get update && apt-get install -y \
     epubcheck \
     && rm -rf /var/lib/apt/lists/*

USER app

# tox-uv makes tox create envs with uv; uv provides the other Pythons
# (3.12 is the system one). Preinstall them so runs don't download them.
RUN pip install tox tox-uv
RUN uv python install 3.8 3.9 3.10 3.11

WORKDIR /src
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
