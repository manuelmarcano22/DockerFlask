FROM debian:8.5

MAINTAINER Kamil Kwiek <kamil.kwiek@continuum.io>

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
    libglib2.0-0 libxext6 libsm6 libxrender1 \
    git mercurial subversion

RUN echo 'export PATH=/opt/conda/bin:$PATH' > /etc/profile.d/conda.sh && \
    wget --quiet https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh

RUN apt-get install -y curl grep vim sed dpkg tmux && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

ENV PATH /opt/conda/bin:$PATH

# Install app dependencies

#Astroconda
RUN /opt/conda/bin/conda config --add channels http://ssb.stsci.edu/astroconda
RUN /opt/conda/bin/conda create -y -n iraf27 python=2.7 iraf pyraf 
RUN /bin/bash -c "source activate /opt/conda/envs/iraf27"

#Dependencies
RUN conda install Flask
RUN conda install bokeh

# Bundle app source
#COPY simpleapp.py /src/simpleapp.py
COPY simpleapp.py /root/simpleapp.py
COPY .tmux.conf /root/.tmux.conf
ADD templates /root/templates/
ADD static /root/static/
ADD images /root/images/


EXPOSE  8000
CMD ["python", "/root/simpleapp.py", "-p 8000"]
