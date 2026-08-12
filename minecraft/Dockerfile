FROM amazoncorretto:25

# Install Python3 for the fake HTTP server
RUN yum install -y python3 && yum clean all

WORKDIR /data

COPY paper.jar /server/paper.jar
COPY plugins /server/plugins
COPY start.sh /start.sh
COPY server.py /server.py

RUN chmod +x /start.sh

EXPOSE 25565

CMD ["/start.sh"]