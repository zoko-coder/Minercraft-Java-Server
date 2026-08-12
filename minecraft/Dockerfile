FROM amazoncorretto:25

WORKDIR /data

COPY paper.jar /server/paper.jar
COPY plugins /server/plugins
COPY start.sh /start.sh

RUN chmod +x /start.sh

EXPOSE 25565

CMD ["/start.sh"]