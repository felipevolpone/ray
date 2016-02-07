FROM ubuntu:14.04
MAINTAINER felipevolpone@gmail.com
ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /home/onhands-alabama

RUN sudo apt-get update
RUN sudo apt-get -y install python-pip python-dev build-essential libfreetype6 libfontconfig1 libpq-dev
RUN sudo apt-get -y install curl git
RUN sudo apt-get -y install postgresql-9.3 postgresql-client-9.3
RUN sudo echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf
RUN sudo echo "host all all 0.0.0.0/0 md5" >> /etc/postgresql/9.3/main/pg_hba.conf
RUN sudo service postgresql start &&\
    sudo -u postgres psql --command "CREATE USER onhands WITH SUPERUSER PASSWORD 'onhands';" &&\
    sudo -u postgres createdb -O onhands onhands &&\
    service postgresql stop

RUN sudo pip install alabama requests pytest

RUN git clone https://github.com/felipevolpone/onhands.git
WORKDIR /home/onhands-alabama/onhands/onhands-core
RUN sudo pip install --editable .
WORKDIR /home/onhands-alabama/onhands/onhands-alabama
RUN sudo pip install --editable .

WORKDIR /home/onhands-test
