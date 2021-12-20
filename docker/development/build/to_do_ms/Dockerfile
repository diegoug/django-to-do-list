FROM ubuntu:20.04
LABEL maintainer="diego.uribe.gamez@gmail.com"
# enviroment variables
ENV TZ="America/Bogota"
ENV DEBIAN_FRONTEND="noninteractive"
# update
RUN apt-get update && apt-get -y upgrade
# basic packages
RUN apt-get -y install build-essential
RUN apt-get -y install libxml2-dev libxmlsec1-dev libxmlsec1-openssl
RUN apt-get -y install python3.9 python3.9-dev
RUN apt-get -y install python3-pkgconfig python3-setuptools python3-pip
RUN apt-get -y install deepin-gettext-tools
RUN apt-get -y install openssh-server
# postgresql packeges
RUN apt-get -y install postgresql libpq-dev postgresql-client postgresql-client-common
# install requirements
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
RUN rm -f /tmp/requirements.txt
# install entry ssh
RUN mkdir /var/run/sshd
COPY entry.tar.gz /entry.tar.gz
RUN tar xzf entry.tar.gz
RUN rm -f entry.tar.gz
RUN chmod 0777 /entry.sh
RUN chmod +x /entry.sh
RUN mkdir /root/.ssh/
# start container commands
EXPOSE 22
ENTRYPOINT ["/entry.sh"]
CMD ["/usr/sbin/sshd", "-D", "-f", "/etc/ssh/sshd_config"]
# work directory
WORKDIR /opt/app