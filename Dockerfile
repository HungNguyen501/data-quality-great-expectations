FROM apache/airflow:2.7.1-python3.11

ARG user_id
ARG group_id

USER root

# Add webserver configuration file
# COPY ./webserver_config.py /opt/airflow/webserver_config.py

# Ignore uid, gid check in image entrypoint
RUN sed -i '238s/^/# /' /entrypoint

RUN userdel airflow
RUN echo "airflow:x:${user_id}:${group_id}:airflow user:/home/airflow:/sbin/nologin" >> /etc/passwd
RUN chown -R ${user_id}:${group_id} /home/airflow
RUN chown -R ${user_id}:${group_id} /opt/airflow

RUN mkdir -p /UID/tmp/multiproc-tmp
RUN chown -R ${user_id}:${group_id} /UID

COPY . /opt/airflow/dags
WORKDIR /opt/airflow/dags

USER airflow

ENV PROMETHEUS_MULTIPROC_DIR=/UID/tmp/multiproc-tmp

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["/bin/sh", "-c"]
