FROM java:8-jre


ENV \
HADOOP_HOME=/usr/local/hadoop 

RUN \
    apt-get update && \
    apt-get install ssh rsync -y

# HADOOP
RUN \
    mkdir -p ${HADOOP_HOME} && \
    cd ${HADOOP_HOME}/.. && \
    HADOOP_VERSION=3.2.0; wget -q \
      https://archive.apache.org/dist/hadoop/core/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz && \
    tar -xf hadoop*.tar.gz -C hadoop --strip-components=1 && \
    echo "Version $(ls | grep hadoop- | sed -e 's/[^0-9 . ]//g')" >> ./hadoop/version.conf && \
    chmod +x ./hadoop/bin/hadoop && \
    rm -rf hadoop*.*

# Second install goes to top TODO
RUN \
  apt-get install -y openssh-server

RUN \
    ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa          && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys   && \
    chmod 0600 ~/.ssh/authorized_keys                 

ADD conf/hadoop /usr/local/hadoop/etc/hadoop
ADD script/hadoop/start-up.sh /usr/local/start-up.sh

WORKDIR ${HADOOP_HOME}

ENTRYPOINT  exec /bin/bash -c "service ssh start;"
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait""