# Elastic Beats

[![Build Status](https://travis-ci.org/dockerlabs/beats.svg?branch=master)](https://travis-ci.org/dockerlabs/beats)

### Environ

Create `.env` file

```sh
LOGSTASH_HOST=logstash:5020
SSL_BEATS_DIR=/etc/ssl/beats
NGINX_STATUS_URL=http://127.0.0.1:8080/nginx_status
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672
```

### Quickstart

```sh
$ make up
```

```sh
$ make logs
```
