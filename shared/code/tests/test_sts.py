import botocore
import unittest
from unittest.mock import patch
from botocore.stub import Stubber, ANY
from shared.aws.sts import create_assumed_role_session

sts_client = botocore.session.get_session().create_client('sts')

class AwsStsTests(unittest.TestCase):

    @patch('shared.aws.sts.boto3.session.Session')
    @patch('shared.aws.sts.boto3.client')
    def test_should_create_default_session_for_same_account(self, client, session):
        client.return_value = sts_client
        with Stubber(sts_client) as stubber:
            stubber.add_response('get_caller_identity', {})
            create_assumed_role_session()
            session.assert_called_with()

    @patch('shared.aws.sts.boto3.session.Session')
    @patch('shared.aws.sts.boto3.client')
    def test_create_assumed_role_session_for_different_account(self, client, session):
        client.return_value = sts_client
        with Stubber(sts_client) as stubber:
            stubber.add_response('get_caller_identity', {'Account': '123456789011'})
            stubber.add_response('assume_role', {
                'Credentials': {
                    'AccessKeyId': 'ASIA3JGZXG3KTZQV65VB',
                    'SecretAccessKey': 'U93KE/LQDmONvlKPbhlW72ho/wbGdGGXgKjaTn2y',
                    'SessionToken': 'token',
                    'Expiration': 3600
                }
            }, {
                'RoleArn': ANY,
                'RoleSessionName': ANY
            })
            create_assumed_role_session('123456789012')
            session.assert_called_with(
                aws_access_key_id='ASIA3JGZXG3KTZQV65VB',
                aws_secret_access_key='U93KE/LQDmONvlKPbhlW72ho/wbGdGGXgKjaTn2y',
                aws_session_token='token'
            )
