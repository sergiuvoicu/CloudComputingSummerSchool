import json
import os
import sys
import csv
import boto3



def read_json(json_file_path: str):
    with open(json_file_path, mode="r", encoding="utf-8-sig") as fr:
        return json.load(fr)


def write_json(filename, data):
    with open(filename, mode="w+") as fw:
        json.dump(data, fw)


def read_csv(csv_file_path: str):
    data = []
    with open(csv_file_path, mode="r", encoding="utf-8-sig") as fr:
        csv_reader = csv.reader(fr)
        for idx, row in enumerate(csv_reader):
            if idx == 0:
                header = [item for item in row[0].split(";")]
            else:
                data_elem = {}
                for item_idx, item in enumerate(row[0].split(";")):
                    data_elem[header[item_idx].lower()] = item
                data.append(data_elem)
    return data


def create_users(users_list: list, version: str = ""):
    is_client = boto3.client("identitystore")
    identity_store = os.environ["identity_store_id"]
    group_id = os.environ["group_id"]
    
    users_data = []
    for user in users_list:
        username = user["email"].split("@")[0]
        display_name = user["name"]
        first_name, last_name = display_name.split(" ")
        user_id = is_client.create_user(
            IdentityStoreId=identity_store,
            UserName=username,
            DisplayName=display_name,
            Name={
                "GivenName": first_name,
                "FamilyName": last_name,
            }
        )["UserId"]

        is_client.create_group_membership(
            IdentityStoreId=identity_store,
            GroupId=group_id,
            MemberId={
                "UserId": user_id
            },
        )

        user_data = {
            "identity_store_id": identity_store,
            "user_id": user,
            "group_id": group_id
        }

        users_data.append(user_data)
    
    filename = f"users_created_{version}.json" if version else "users_created.json"
    write_json(filename, users_data)


def get_users(version: str = ""):
    is_client = boto3.client("identitystore")
    identity_store = os.environ["identity_store_id"]
    group_id = os.environ["group_id"]
    users_data = []
    token = True
 
    while token:
        if isinstance(token, bool):
            response = is_client.list_users(
                IdentityStoreId=identity_store
            )
        elif isinstance(token, str):
            response = is_client.list_users(
                IdentityStoreId=identity_store,
                NextToken=token
            )
        users = response["Users"]
        token = response.get("NextToken") or None
        
        for user in users:
            users_data.append({
                "identity_store_id": user["IdentityStoreId"],
                "user_id": user["UserId"],
                "username": user["UserName"],
                "display_name": user["DisplayName"]
            })

    filename = f"identity_store_users_{version}.json" if version else "identity_store_users.json"
    write_json(filename, users_data)


def delete_users(users_data: dict, version: str = ""):
    is_client = boto3.client("identitystore")
    
    deleted_users = []
    for user in users_data:
        is_client.delete_user(
            IdentityStoreId=user["identity_store_id"],
            UserId=user["user_id"]
        )
        deleted_users.append(user)

    filename = f"deleted_users_{version}.json" if version else "deleted_users.json"
    write_json(filename, deleted_users)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        operation, filename = sys.argv[1], sys.argv[2]

        if operation == "get_users":
            version = sys.argv[2]
        elif len(sys.argv) == 4:
            version = sys.argv[3]
        else:
            version = ""

        if operation == "create_only":
            create_users(read_json(filename), version)
        elif operation == "read_only":
            to_replace = f"_{version}.json" if version else ".json"
            write_json(filename.replace(".csv", to_replace), read_csv(filename))
        elif operation == "get_users":
            get_users(version)
        elif operation == "create_users":
            create_users(read_csv(filename), version)
        elif operation == "delete_users":
            delete_users(read_json(filename), version)
