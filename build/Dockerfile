FROM apache/airflow:2.7.3-python3.11

ARG USER_ID
ARG GROUP_ID

# ENV http_proxy http://10.40.81.2:8088
# ENV https_proxy http://10.40.81.2:8088
ENV TZ=Asia/Ho_Chi_Minh
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
ENV SPARK_HOME=/home/airflow/.local/lib/python3.11/site-packages/pyspark
ENV HADOOP_CONF_DIR=/opt/airflow/hadoop
ENV HADOOP_USER_NAME=zdeploy
ENV COMPANY_FOLDER=mrroot501
ENV PYTHONPATH=${PYTHONPATH}:/opt/airflow/${COMPANY_FOLDER}

USER root

# Set timezone
RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && echo ${TZ} > /etc/timezone

# Install java
RUN apt-get update \
    && apt-get install -y --no-install-recommends openjdk-11-jre-headless \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ignore uid, gid check in image entrypoint
RUN sed -i '238s/^/# /' /entrypoint

RUN userdel airflow
RUN echo "airflow:x:${USER_ID}:${GROUP_ID}:airflow user:/home/airflow:/sbin/nologin" >> /etc/passwd \
    && chown -R ${USER_ID}:${GROUP_ID} /home/airflow \
    && chown -R ${USER_ID}:${GROUP_ID} /opt/airflow \
    && mkdir -p /UID/tmp/multiproc-tmp \
    && chown -R ${USER_ID}:${GROUP_ID} /UID

COPY . /opt/airflow/${COMPANY_FOLDER}
WORKDIR /opt/airflow

USER airflow

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r ${COMPANY_FOLDER}/requirements.txt

ENTRYPOINT ["/bin/sh", "-c"]
