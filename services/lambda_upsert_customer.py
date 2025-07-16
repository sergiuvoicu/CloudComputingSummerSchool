import json
import os
import boto3

from aws_lambda_powertools import Logger
from http import HTTPStatus


dynamodb_res = boto3.resource("dynamodb")
customers_table = dynamodb_res.Table(os.environ["environment"] + "customers")


def upsert_customer(customer_data):
    customers_table.put_item(Item=customer_data)


def upsert_customer_handler(event, _):

    Logger().info(event)
    request_body = json.loads(event["body"])

    upsert_customer(request_body)

    response = {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({
            "message": "Customer data inserted successfully!"
        })
    }
    Logger().info(response)
    return response
