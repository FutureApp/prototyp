FROM danisla/hadoop:2.9.0

RUN \
    apt-get update && \
    apt-get install net-tools



ENV HIVE_VERSION=3.1.1 
ENV HIVE_HOME="/usr/local/hive"
RUN \
cd ${HADOOP_COMMON_HOME}/.. && \
wget -q \
  http://www.gutscheine.org/mirror/apache/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz && \
mkdir hive && \
tar -xf apache-hive*.tar.gz -C hive --strip-components=1 && \
echo "Version $(ls | grep apache-hive- | sed -e 's/[^0-9 . ]//g')" >> ./hive/version.conf && \
cd hive && export HIVE_HOME=$(pwd) && export PATH=$HIVE_HOME/bin:$PATH && cd .. && \
rm -rf apache-hive*.*


# DERBY 
ENV DERBY_VERSION=10.14.2.0
ENV DERBY_HOME="/usr/local/derby"
ENV PATH="${PATH}:/usr/local/hadoop/bin:\
/usr/local/hive/bin:/usr/local/derby/bin:"

RUN \
    cd ${HADOOP_COMMON_HOME}/.. && \
    wget -q  \
      http://ftp.halifax.rwth-aachen.de/apache//db/derby/db-derby-${DERBY_VERSION}/db-derby-${DERBY_VERSION}-bin.tar.gz && \
    mkdir derby && \
    tar -xf db-derby*.tar.gz -C derby --strip-components=1 && \
    echo "Version $(ls | grep db-derby- | sed -e 's/[^0-9 . ]//g')" >> ./derby/version.conf && \
    cd derby && PATH=$DERBY_HOME/bin:$PATH && cd .. && \
    rm -rf db-derby*.*

#SO on
EXPOSE 10000