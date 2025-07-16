import csv
import json
import os
import boto3

from datetime import datetime, timezone
from http import HTTPStatus
from aws_lambda_powertools import Logger

s3_client = boto3.client("s3")
dynamodb_res = boto3.resource("dynamodb")

customers_table = dynamodb_res.Table(os.environ["environment"] + "customers")


def get_customers():
    return customers_table.scan()["Items"]


def generate_report_handler(event, _):

    Logger().info(event)
    customers = get_customers()

    if not customers:
        return {
            "statusCode": HTTPStatus.NOT_FOUND,
            "body": {
                "message": "No customer found!"
            }
        }

    timestamp = datetime.now(tz=timezone.utc).isoformat()
    local_filename = f"/tmp/customers_{timestamp}.csv"
    header = customers[0].keys()

    with open(local_filename, "w+") as fw:
        writer = csv.writer(fw)
        writer.writerow(header)

        for customer in customers:
            writer.writerow(customer.values())

    s3_client.upload_file(
        local_filename,
        os.environ["s3_bucket_name"],
        f"{os.environ['remote_path']}/{os.path.basename(local_filename)}"
    )

    return {
        "statusCode": HTTPStatus.OK,
        "body": json.dumps({
            "message": "Customers report generated successfully!"
        })
    }
