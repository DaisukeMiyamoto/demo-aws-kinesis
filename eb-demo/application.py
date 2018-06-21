from flask import Flask, request
import json
import boto3
import sys
from datetime import datetime
from time import sleep


class Kinesis():
    def __init__(self, stream_name, region='ap-northeast-1'):
        self.kinesis_client = boto3.client('kinesis', region_name=region)
        self.stream_name = stream_name
    
    def put(self, data):
        response = self.kinesis_client.put_record(
            StreamName=self.stream_name,
            Data=data,
            PartitionKey=data
        )
        return response


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


class UserTable():
    def __init__(self):
        self.ad_path = ''
        self.default_ad_uri = 'ad0.jpeg'
        self.users = {
            1: {
                'user_id': '1',
                'country code': 'US',
                'state/region': 'WA',
                'ad_id': '1',
                'ad_uri': 'ad1.jpeg'
            },
            2: {
                'user_id': '2',
                'country code': 'US',
                'state/region': 'NY',
                'ad_id': '2',
                'ad_uri': 'ad2.png'
            },
            3: {
                'user_id': '3',
                'country code': 'US',
                'state/region': 'MA',
                'ad_id': '1',
                'ad_uri': 'ad1.jpeg'
            },
            4: {
                'user_id': '4',
                'country code': 'US',
                'state/region': 'TX',
                'ad_id': '1',
                'ad_uri': 'ad1.jpeg'
            }
        }
        
    def get_ad_uri(self, user_id):
        if user_id in self.users:
            return self.ad_path + self.users[user_id]['ad_uri']
        else:
            return self.ad_path + self.default_ad_uri

    def get_userinfo_json(self, user_id):
        if user_id in self.users:
            return_dict = dict(self.users[user_id])
        else:
            return_dict = {'Error': 'User ID Mismatch', 'ad_uri': self.default_ad_uri}

        return_dict.update({'timestamp': datetime.utcnow().isoformat()})
        return json.dumps(return_dict)


# kinesis = Kinesis()
kinesis = KinesisFirehose(stream_name='demo-aws-ad-firehose')
user_table = UserTable()
DEBUG_MODE = False
application = Flask(__name__)


@application.route('/')
def get_root():
    return 'Hello\n'


@application.route('/ad')
def get_ad():
    sleep(0.04)
    try:
        user_id = int(request.args.get('user_id', '0'))
        kinesis.put(user_table.get_userinfo_json(user_id)+'\n')
        return '%s\n' % (user_table.get_ad_uri(user_id))
    except Exception as e:
        return 'Error: %s' % (e.args)
        

@application.route('/debug/userinfo')
def get_userinfo():
    user_id = int(request.args.get('user_id', '0'))
    return '%s\n' % (user_table.get_userinfo_json(user_id))


@application.route('/debug/kinesis')
def put_kinesis(): 
    user_id = int(request.args.get('user_id', '0'))
    send_json = user_table.get_userinfo_json(user_id)
    response = kinesis.put(send_json)
    return '%s\n%s\n' % (send_json, response)


@application.route('/debug/adnowait')
def get_ad_nowait():
    try:
        user_id = int(request.args.get('user_id', '0'))
        kinesis.put(user_table.get_userinfo_json(user_id)+'\n')
        return '%s\n' % (user_table.get_ad_uri(user_id))
    except Exception as e:
        return 'Error: %s' % (e.args)


if __name__ == '__main__':
    application.run()
