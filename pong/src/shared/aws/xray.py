import os
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all


def configure_xray(service):
    if not os.environ.get('DISABLE_XRAY', False):
        xray_recorder.configure(
            context_missing='LOG_ERROR',
            service=service
        )
        patch_all()
