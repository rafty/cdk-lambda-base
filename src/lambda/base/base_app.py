import json
from aws_lambda_powertools import Logger

logger = Logger()


@logger.inject_lambda_context(log_event=True)
def handler(event, context):
    # print('request: {}'.format(json.dumps(event)))
    logger.debug('debug')
    logger.info('info')

    return {}
