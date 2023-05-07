FROM registry.redhat.io/ubi8/openjdk-11:latest

USER root
# need to install python2.7 for ycsb
RUN \
    microdnf install -y git-core wget tar python2 && \
    microdnf clean all && \
    ln -sf /usr/bin/python2.7 /usr/bin/python

# clone ycsb and build fdb binding
RUN \
    wget  https://github.com/adobe/newsql-benchmark/raw/main/ansible/roles/loadgen_ycsb_install/files/ycsb-foundationdb-binding-0.18.0-SNAPSHOT.tar.gz && \
    tar -xvf ycsb-foundationdb-binding-0.18.0-SNAPSHOT.tar.gz 


# install fdb client
RUN \
    rpm -i https://github.com/apple/foundationdb/releases/download/7.1.31/foundationdb-clients-7.1.31-1.el7.x86_64.rpm


# command that just loops and does nothing, so container does not exit
CMD ["tail", "-f", "/dev/null"]



# docker build -t ycsb .

