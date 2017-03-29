##
## hepsw/cc7-base is a WIP image for CERN CentOS-7
##
FROM centos:7
MAINTAINER Sebastien Binet "binet@cern.ch"

# add CERN CentOS yum repo
ADD http://linux.web.cern.ch/linux/centos7/CentOS-CERN.repo /etc/yum.repos.d/CentOS-CERN.repo
ADD http://linuxsoft.cern.ch/cern/centos/7.1/os/x86_64/RPM-GPG-KEY-cern /tmp/RPM-GPG-KEY-cern

RUN /usr/bin/rpm --import /tmp/RPM-GPG-KEY-cern && \
    /bin/rm /tmp/RPM-GPG-KEY-cern

# RUN /usr/bin/yum groups mark convert && \
#     /usr/bin/yum --enablerepo=*-testing clean all && \
#     /usr/bin/yum groupinstall --skip-broken -y 'CERN Base Tools' && \
#     /usr/bin/yum groupinstall --skip-broken -y --exclude libwbclient.i686 'Software Development Workstation (CERN Recommended Setup)' && \
#     /usr/bin/yum --enablerepo=*-testing clean all

RUN yum update -y && \
	yum clean all

##Extra
RUN yum -y update
RUN yum -y install \
           file which

RUN yum -y install binutils-devel gcc gcc-c++ gcc-gfortran git make patch python-devel \
	   glibc.i686 zlib.i686 ncurses-libs.i686 bzip2-libs.i686 uuid.i686 libxcb.i686 \
	   libXmu.so.6 libncurses.so.5 tcsh


#These are needed to build IRAF
RUN yum -y install \
           bzip2-devel \
           libXpm-devel libXft-devel libXext-devel \
           libxml2-devel \
           libuuid-devel \
           ncurses-devel \
           texinfo \
           wget \
	   bzip2 sudo passwd bc csh vim libXScrnSaver evince


#RUN yum -y install libxslt-devel libXt-devel zip

##TO install Anaconda with Python 3.4
#RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
#    wget --quiet https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh -O ~/anaconda.sh
#RUN /bin/bash ~/anaconda.sh -b -p /opt/conda && \
#    rm ~/anaconda.sh
#ENV PATH /opt/conda/bin:$PATH

##To install minicoda python 3.5
#RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
#    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  -O ~/miniconda.sh && \
#    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
#    rm ~/miniconda.sh
#RUN /opt/conda/bin/conda  install -y -c astropy python-cpl=0.7.2
#ENV PATH /opt/conda/bin:$PATH

## Intall minicoda python 2.7
RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh  -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

ENV PATH /opt/conda/bin:$PATH
##With iraf
RUN /opt/conda/bin/conda config --add channels http://ssb.stsci.edu/astroconda
##Install
ENV PATH /opt/conda/bin:$PATH

#Astroconda
RUN /opt/conda/bin/conda config --add channels http://ssb.stsci.edu/astroconda
RUN /opt/conda/bin/conda create -y -n iraf27 python=2.7 iraf pyraf Flask bokeh

WORKDIR "/root"
ADD login.cl /root/login.cl
#RUN /opt/conda/envs/iraf27/bin/mkiraf

# Bundle app source
COPY simpleapp.py /root/simpleapp.py
COPY .tmux.conf /root/.tmux.conf
ADD templates /root/templates/
ADD static /root/static/
ADD images /root/images/

EXPOSE  8080
ADD start.sh /root/start.sh
RUN chmod +x start.sh
ENTRYPOINT ["/bin/bash","start.sh"]
