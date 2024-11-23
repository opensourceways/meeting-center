FROM openeuler/openeuler:22.03

ARG user=meetingcenter
ARG group=meetingcenter
ARG uid=1000
ARG gid=1000


# 1.install
RUN yum install -y openssl openssl-devel tzdata python3-devel mariadb-devel python3-pip gcc
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -d /home/meetingcenter/ -s /sbin/nologin -m ${user}

# 2.copy
COPY . /home/meetingcenter/meeting-center/
RUN rm -rf /home/meetingcenter/meeting-center/Dockerfile

# 3.install
RUN pip3 install -r /home/meetingcenter/meeting-center/requirements.txt && rm -rf /home/meetingcenter/meeting-center/requirements.txt

# 4.clean
RUN yum remove -y gcc python3-pip procps-ng
RUN rm -rf /usr/bin/kill
RUN ln -s /usr/bin/python3 /usr/bin/python

RUN chmod -R 550 /home/meetingcenter/meeting-center/ && \
    chown -R ${user}:${group} /home/meetingcenter/meeting-center/
RUN chmod 550 /home/meetingcenter/meeting-center/manage.py && \
    chown ${user}:${group} /home/meetingcenter/meeting-center/manage.py
RUN chmod 550 /home/meetingcenter/meeting-center/docker-entrypoint.sh && \
    chown ${user}:${group} /home/meetingcenter/meeting-center/docker-entrypoint.sh
RUN mkdir -p /home/meetingcenter/meeting-center/deploy/static &&  \
    chmod -R 750 /home/meetingcenter/meeting-center/deploy &&  \
    chown -R ${user}:${group} /home/meetingcenter/meeting-center/deploy
RUN echo > /etc/issue && echo > /etc/issue.net && echo > /etc/motd
RUN sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   90/' /etc/login.defs
RUN echo 'set +o history' >> /root/.bashrc
RUN rm -rf /tmp/*
RUN history -c && echo "set +o history" >> /home/meetingcenter/.bashrc  && echo "umask 027" >> /home/meetingcenter/.bashrc && source /home/meetingcenter/.bashrc

# 5.Run server
WORKDIR /home/meetingcenter/meeting-center
ENV LANG=en_US.UTF-8
USER ${uid}:${gid}

ENTRYPOINT ["/home/meetingcenter/meeting-center/docker-entrypoint.sh"]
CMD ["uwsgi", "--ini", "/home/meetingcenter/meeting-center/deploy/production/uwsgi.ini"]
EXPOSE 8080
