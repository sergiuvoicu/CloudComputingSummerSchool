import json
from aws_lambda_powertools import Logger
from http import HTTPStatus


def hello_world_handler(event, _):

    Logger().info(event)
    response = {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({
            "message": "Hello World!"
        })
    }
    Logger().info(response)
    return response
