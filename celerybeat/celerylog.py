#!/usr/bin/env python

import argparse
import datetime
import sys

from celery import Celery


def task_processor(options, state, event):
    state.event(event)
    task = state.tasks.get(event['uuid'])

    def _parse_dtime(timestamp):
        if not isinstance(timestamp, float):
            return timestamp
        return datetime.datetime.fromtimestamp(timestamp).isoformat()

    context = task.as_dict()
    worker = context['worker']

    for timefield in ('started', 'received', 'succeeded', 'timestamp'):
        if timefield in context:
            context[timefield] = _parse_dtime(context[timefield])

    context.update({
        'worker': {
            'id': worker.id,
            'hostname': worker.hostname,
            'heartbeats': worker.heartbeats,
            'freq': worker.freq,
            'heartbeat_expires': _parse_dtime(worker.heartbeat_expires),
            'expire_window': worker.expire_window
        },
        'exception': {
            'message': context['exception']
        }
    })

    logstash_host, logstash_port = options.logstash_url.split(':')
    # json.dumps(context)


def main(args):
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        '-b', '--broker-url',
        help='Broker url',
        default='amqp://guest:guest@localhost:5672')

    parser.add_argument(
        '-l', '--logstash-host',
        help='Logstash host',
        default='logstash:5000')

    options = parser.parse_args(args)
    app = Celery(broker=options.broker_url)
    state = app.events.State()

    def _task_processor(event):
        task_processor(options, state, event)

    with app.connection() as connection:
        app.events.Receiver(connection, handlers={
            '*': state.event,
            'task-succeeded': _task_processor,
            'task-failed': _task_processor,
            'task-revoked': _task_processor
        }).capture(limit=None, timeout=None, wakeup=True)

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
