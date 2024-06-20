FROM mmore500/docker-texlive-full:sha-ea45eb5

COPY . /opt/llms-for-data-extraction/tex

SHELL ["/bin/bash", "-c"]

# Define default working directory.
WORKDIR /opt/llms-for-data-extraction/tex

# Prevent interactive time zone config.
# adapted from https://askubuntu.com/a/1013396
ENV DEBIAN_FRONTEND=noninteractive

RUN \
  echo 'Acquire::http::Timeout "60";' >> "/etc/apt/apt.conf.d/99timeout" \
    && \
  echo 'Acquire::ftp::Timeout "60";' >> "/etc/apt/apt.conf.d/99timeout" \
    && \
  echo 'Acquire::Retries "100";' >> "/etc/apt/apt.conf.d/99timeout" \
    && \
  echo "buffed apt-get resiliency"

RUN \
  find /etc/apt -type f -name '*.list' -exec sed -i 's/\(^deb.*-backports.*\)/#\1/; s/\(^deb.*-updates.*\)/#\1/; s/\(^deb.*-proposed.*\)/#\1/; s/\(^deb.*-security.*\)/#\1/' {} + \
    && \
  rm -rf /var/lib/apt/lists/* \
    && \
  echo "removed -backports, -updates, -proposed, -security repositories"

# magic to fix java installation conflict in subsequent apt install
# see https://github.com/geerlingguy/ansible-role-java/issues/64
RUN \
  apt-get update -q --allow-unauthenticated \
    && \
  apt-get install -qy --no-install-recommends \
    man \
    && \
  rm -rf /var/lib/apt/lists/* \
    && \
  mkdir /usr/share/man/man1/

RUN \
  apt-get update -q --allow-unauthenticated \
    && \
  apt-get install -qy --no-install-recommends \
    bibtool \
    git \
    make \
    moreutils \
    nodejs \
    pcregrep \
    pdftk \
    && \
  rm -rf /var/lib/apt/lists/*

CMD ["bash"]
