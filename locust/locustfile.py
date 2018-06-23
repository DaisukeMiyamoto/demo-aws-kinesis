# -*- coding: utf-8 -*-
"""
$ ./start_locust.py -H http://hogehoge.com -c 100 -r 50
"""

from locust import HttpLocust, TaskSet, task
from locust.events import request_success
from datetime import datetime
import boto3
import json
import time
from random import random


class KinesisFirehose():
    def __init__(self, stream_name, region='ap-northeast-1'):
        self.kinesis_client = boto3.client('firehose', region_name=region)
        self.stream_name = stream_name
    
    def put(self, data):
        response = self.kinesis_client.put_record(
            DeliveryStreamName=self.stream_name,
            Record={
                'Data': data
            }
        )
        return response


def send_kinesis_success_fire(time):
    request_success.fire(
        request_type='PUT',
        name='Kinesis',
        response_time=time,
        response_length=0
    )


class SimpleSet(TaskSet):
    @task
    def hello(self):
        self.client.get('/')


class NowaitSet(TaskSet):
    @task
    def user(self):
        self.client.get('/debug/adnowait?user_id=1')


kinesis = KinesisFirehose(stream_name='demo-aws-adclick-firehose')
class UserVarietySet(TaskSet):
    def on_start(self):
        self.send_click = True
        
        if self.send_click:
            self.kinesis = kinesis

    def _get_ad(self, user_id, ad_id=0, rate=0.1):
        self.client.get('/ad?user_id=%d' % user_id)

        if self.send_click:
            if random() < rate:
                start_at = time.time()
                record = {'timestamp': datetime.utcnow().isoformat(), 'user_id': str(user_id), 'ad_id': str(ad_id)}
                json_record = json.dumps(record)
                response = self.kinesis.put(json_record)
                send_kinesis_success_fire(int((time.time() - start_at) * 1000))

    @task(1)
    def user1(self):
        self._get_ad(1, 1, 0.1)

    @task(8)
    def user2(self):
        self._get_ad(2, 2, 0.2)

    @task(3)
    def user3(self):
        self._get_ad(3, 1, 0.05)


class ClickWithKinesisFirehose(TaskSet):
    def on_start(self):
        self.kinesis = kinesis

    @task
    def put(self):
        start_at = time.time()
        record = {'timestamp': datetime.utcnow().isoformat(), 'user_id': '1', 'ad_id': '1'}
        json_record = json.dumps(record)
        response = self.kinesis.put(json_record)
        send_kinesis_success_fire(int((time.time() - start_at) * 1000))


class WebsiteUser(HttpLocust):
    task_set = UserVarietySet
    # task_set = SimpleSet
    # task_set = NowaitSet
    # task_set = ClickWithKinesisFirehose
    min_wait = 0
    max_wait = 10

