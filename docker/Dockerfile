FROM python:3.6
MAINTAINER Axel Sirota <axel.sirota@gmail.com>

# Prevent dpkg errors
ENV TERM=xterm-256color
ENV DEBIAN_FRONTEND noninteractive

# Install Python runtime

RUN apt-get update && apt-get install -qy --no-install-recommends \
    -o APT::Install-Suggests="false" -o APT::Install-Recommends="false" \
    checkinstall python3 python3-pip python3-dev build-essential python3-setuptools libssl-dev \
    libffi-dev openssh-client openssh-server aptitude && aptitude install ssh\
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
# Upgrade PIP in virtual environment to latest version
RUN python3 -m pip install virtualenv && \
    python3 -m virtualenv /venv && \
    . /venv/bin/activate && \
    pip install pip --upgrade && \
    pip install wheel --upgrade

ENV DEBIAN_FRONTEND teletype
ENV WHEELHOUSE=/wheelhouse PIP_WHEEL_DIR=/wheelhouse PIP_FIND_LINKS=/wheelhouse XDG_CACHE_HOME=/cache
VOLUME /wheelhouse

COPY . /app
WORKDIR /app

RUN . /venv/bin/activate && \
    pip install -e .

# Add test entrypoint script
COPY docker/scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh \
    && mkdir -p /reports

EXPOSE 5000

# Set defaults for entrypoint and command string
ENTRYPOINT ["entrypoint.sh"]

# OUTPUT: Reports are output here
VOLUME /reports