# -*- coding: utf-8 -*-

from locust import HttpLocust, TaskSet, task
from locust.events import request_success
import boto3
import json
import time
import datetime


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

class SimpleSet(TaskSet):
    @task
    def hello(self):
        self.client.get('/')


class NowaitSet(TaskSet):
    @task
    def user(self):
        self.client.get('/debug/adnowait?user_id=1')


class UserVarietySet(TaskSet):
    @task(1)
    def user1(self):
        self.client.get('/ad?user_id=1')

    @task(8)
    def user2(self):
        self.client.get('/ad?user_id=2')

    @task(3)
    def user3(self):
        self.client.get('/ad?user_id=3')


class ClickWithKinesisFirehose(TaskSet):

    def on_start(self):
        self.kinesis = KinesisFirehose(stream_name='demo-aws-adclick-firehose')

    @task
    def put(self):
        start_at = time.time()
        record = {
            'timestamp': datetime.utcnow().isoformat(),
            'user_id': '1',
            'ad_id': '1'
        }
        json_record = json.dumps(record)
        response = self.kinesis.put(json_record)
        request_success.fire(
            request_type='PUT',
            name=self.kinesis.stream_name,
            response_time=int((time.time() - start_at) * 1000),
            response_length=len(response)
        )


class UserVarietyClickSet(TaskSet):

    def on_start(self):
        self.kinesis = boto3.client('firehose', region_name='ap-northeast-1')


class WebsiteUser(HttpLocust):
    # task_set = UserVarietySet
    # task_set = SimpleSet
    # task_set = NowaitSet
    task_set = ClickWithKinesisFirehose
    min_wait = 0
    max_wait = 10

