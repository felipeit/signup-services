FROM python:3.10 as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG POETRY_VERSION=1.1.13

# VSCode users:
# Before rebuild your devcontainer
# make sure poetry.lock is up-to-date
# (use command make update)

# For VSCode Docker Extension to work
# Please check https://aka.ms/vscode-remote/containers/non-root
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME | true \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME | true \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python3-openssl libpq-dev libcurl4-openssl-dev


FROM base
RUN pip install -U pip poetry

RUN mkdir /application

WORKDIR /application

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install
