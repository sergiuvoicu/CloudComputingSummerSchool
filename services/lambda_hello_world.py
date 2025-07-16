from aws_lambda_powertools import Logger
from http import HTTPStatus


def hello_world_handler(event, _):

    Logger().info(event)
    response_body = "Hello World!"

    response = {
        "statusCode": HTTPStatus.OK,
        "body": response_body
    }
    Logger().info(response)
    return response
