FROM rackspacedot/python37
USER root

RUN apt-get update
RUN apt-get -y install locales && \
  localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install flask
RUN pip install SQLAlchemy
RUN pip install Flask-SQLAlchemy
RUN pip install Flask-Cors
RUN pip install Flask-JWT
RUN pip install marshmallow
RUN pip install marshmallow-sqlalchemy
RUN pip install flask-marshmallow
