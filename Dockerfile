FROM ubuntu:14.04
MAINTAINER felipevolpone@gmail.com
ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /home/alabama
ADD . /home/alabama

RUN ./install.sh