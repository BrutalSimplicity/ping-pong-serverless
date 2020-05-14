import boto3
import time


def create_assumed_role_session(account_id=None, cross_account_role='swa/SWACSCloudAdmin'):
    client = boto3.client('sts')
    caller_identity = client.get_caller_identity()
    caller_identity_account_id = caller_identity.get('Account', None)
    if ((account_id is None) or str(caller_identity_account_id) == str(account_id)):
        '''
            if the account id was not supplied, or the account_id is the same account
            where this lambda is running, return the default client, otherwise
            try to assume-role into the account_id
        '''
        return boto3.session.Session()

    # request is for another account, assume role, and return s3 client.
    role_arn = "arn:aws:iam::{}:role/{}"\
        .format(
            account_id,
            cross_account_role
        )
    assume_role_response = client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="ec-landing-zone-{}"
                        .format(int(round(time.time() * 1000)))
    )
    credentials = assume_role_response.get("Credentials")
    return boto3.session.Session(
        aws_access_key_id=credentials.get('AccessKeyId'),
        aws_secret_access_key=credentials.get('SecretAccessKey'),
        aws_session_token=credentials.get('SessionToken')
    )


def client(service, account_id=None, cross_account_role='swa/SWACSCloudAdmin'):
    ''' client '''
    session = create_assumed_role_session(account_id, cross_account_role)
    return session.client(service)
