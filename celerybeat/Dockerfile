FROM celery

COPY celerylog.py /usr/bin/celerylog
CMD ["/bin/bash", "-c", "celerylog -b $CELERY_BROKER_URL -l $LOGSTASH_HOST"]
