FROM condaforge/mambaforge:latest

LABEL maintainer="Ivan Ogasawara <ivan.ogasawara@gmail.com>"
LABEL org.opencontainers.image.title="TimeBank"
LABEL org.opencontainers.image.authors="Open Science Labs Team"
LABEL org.opencontainers.image.source="https://github.com/osl-incubator/timebank"
LABEL org.opencontainers.image.version="latest"
LABEL org.opencontainers.image.description="Time Bank for Open Science/Source communities"
LABEL org.osl.timebank.version="latest"

# it is the default, but using it here to have it explicitly
USER root

SHELL ["/bin/bash", "-c"]
# Use bash in Dockerfile RUN commands and make sure bashrc is sourced when
# executing commands with /bin/bash -c
# Needed to have the micromamba activate command configured etc.

ENV ENV_NAME=timebank-web
ENV DEBIAN_FRONTEND=noninteractive

ARG UID=1000
ARG GID=1000

RUN apt-get update -y \
  && apt-get install -y \
    build-essential \
    zip \
    make \
    cron \
    curl \
    wget \
    sudo \
    tini \
  && rm -rf /var/lib/apt/lists/* \
    /var/cache/apt/archives \
    /tmp/* \
  && addgroup --gid ${GID} tb \
  && useradd --uid ${UID} --gid ${GID} -ms /bin/bash tb \
  && mkdir -p /opt/services \
  && chmod -R a+rwx /opt/conda /opt/services/ \
  && export ENV_NAME="$ENV_NAME" \
  && echo "tb ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/tb \
  && chmod 0440 /etc/sudoers.d/tb

USER tb

ENV PATH /opt/conda/envs/$ENV_NAME/bin:$PATH
ENV PYTHONPATH='/opt/services/timebank:/opt/services/'

RUN mkdir -p /opt/services/
COPY --chown=tb:tb src/timebank-web/ /opt/services/timebank
COPY --chown=tb:tb containers/web/scripts /opt/services/timebank/scripts
COPY --chown=tb:tb poetry.lock /opt/services/timebank/
COPY --chown=tb:tb pyproject.toml /opt/services/timebank/
COPY --chown=tb:tb conda/ /opt/services/timebank/conda

WORKDIR /opt/services/timebank

RUN mamba env create -n $ENV_NAME --file ./conda/web.yaml \
  && poetry install --only web \
  && conda clean --all \
  && find /opt/conda/ -type f,l -name '*.pyc' -delete \
  && find /opt/conda/ -type f,l -name '*.js.map' -delete \
  && rm -rf /opt/conda/pkgs /tmp/*

RUN echo "source /opt/services/timebank/scripts/entrypoint.sh" > ~/.bashrc

ENTRYPOINT ["tini", "--", "/opt/services/timebank/scripts/entrypoint.sh"]
CMD ["./scripts/run.sh"]
