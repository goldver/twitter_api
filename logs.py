#!/usr/bin/python3

import logging
import sys

logging.getLogger('botocore.vendored.requests.packages.urllib3').setLevel(logging.CRITICAL)
logging.getLogger('botocore.vendored.credentials').setLevel(logging.ERROR)

handlers = [logging.StreamHandler(sys.stdout)]

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)-15s] [%(filename)-s:%(lineno)-d] %(levelname)-s - %(message)s',
    handlers=handlers
)

logger = logging.getLogger('md-aws_ml')


def shutdown():
    for handler in logger.handlers:
        handler.close()
        logger.removeFilter(handler)
