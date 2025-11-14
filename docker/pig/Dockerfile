FROM bde2020/hadoop-base:2.0.0-hadoop3.2.1-java8

ENV PIG_VERSION=0.17.0
ENV PIG_HOME=/opt/pig-${PIG_VERSION}
ENV PATH="${PIG_HOME}/bin:${PATH}"
ENV HADOOP_CONF_DIR=/etc/hadoop
ENV PIG_CLASSPATH=/etc/hadoop

ADD https://archive.apache.org/dist/pig/pig-${PIG_VERSION}/pig-${PIG_VERSION}.tar.gz /tmp/pig.tgz
RUN tar -xzf /tmp/pig.tgz -C /opt && rm -f /tmp/pig.tgz

WORKDIR /workspace
