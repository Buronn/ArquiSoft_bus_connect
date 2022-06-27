FROM alpine:3.16.0
COPY . /app
WORKDIR /app
ARG SSHPASS
ARG USER
ARG SERVER
ENV USER $USER
ENV SERVER $SERVER
ENV SSHPASS $SSHPASS
RUN apk add openssh
RUN apk add --update --no-cache sshpass
EXPOSE 5000
CMD sh socket.sh