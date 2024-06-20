FROM mmore500/dishtiny:sha-7f3f5c8

USER root

COPY . /opt/llms-for-data-extraction

RUN \
  npm install -g \
    bibtex-tidy@1.8.5 \
    && \
  echo "installed npm dependencies"

RUN \
  python3 -m pip install -r /opt/llms-for-data-extraction/requirements.txt \
    && \
  echo "installed python dependencies"

RUN \
  apt-get update -q --allow-unauthenticated \
    && \
  apt-get install -qy --no-install-recommends \
    gawk \
    ghostscript \
    && \
  rm -rf /var/lib/apt/lists/*

USER user

# Define default working directory.
WORKDIR /opt/llms-for-data-extraction
