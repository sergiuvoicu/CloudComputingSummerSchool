import json
import sys
import csv
import boto3
import random



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
    iam_client = boto3.client("iam")
    users_data = []
    for user in users_list:
        username = user["email"].split("@")[0]
        user = iam_client.create_user(UserName=username)["User"]
        user["CreateDate"] = user["CreateDate"].isoformat(timespec="seconds")
        iam_client.add_user_to_group(
            UserName=username,
            GroupName="SummerSchoolCandidates"
        )
        iam_client.add_user_to_group(
            UserName=username,
            GroupName="SummerSchoolInfrastructureDeployment"
        )
        access_key = iam_client.create_access_key(UserName=username)["AccessKey"]
        access_key["CreateDate"] = access_key["CreateDate"].isoformat(timespec="seconds")
        
        randpass = f"Ch4ng3Th!sP4ssw0rd{"".join([chr(random.randint(65, 122)) for _ in username])}"

        iam_client.create_login_profile(
            UserName=username,
            Password=randpass,
            PasswordResetRequired=True
        )

        user_data = {
            "user_details": user,
            "password_details": randpass,
            "user_groups": ("SummerSchoolCandidates", "SummerSchoolInfrastructureDeployment"),
            "access_key_details": access_key

        }

        users_data.append(user_data)
    
    filename = f"users_created_{version}.json" if version else "users_created.json"
    write_json(filename, users_data)


def delete_users(users_list: list, version: str = ""):
    iam_client = boto3.client("iam")
    users_data = []
    for user in users_list:
        username = user["user_details"]["UserName"]
        access_key_id = user["access_key_details"]["AccessKeyId"]
        iam_client.delete_access_key(
            UserName=username,
            AccessKeyId=access_key_id
        )
        iam_client.delete_login_profile(
            UserName=username
        )
        for group in user["user_groups"]:
            iam_client.remove_user_from_group(
                GroupName=group,
                UserName=username
            )
        iam_client.delete_user(UserName=username)

        users_data.append({
            "username": username,
            "access_key_id": access_key_id
        })

    filename = f"users_deleted_{version}.json" if version else "users_created.json"
    write_json(filename, users_data)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        operation, filename = sys.argv[1], sys.argv[2]

        version = sys.argv[3] if len(sys.argv) == 4 else ""

        if operation == "create_only":
            create_users(read_json(filename), version)
        elif operation == "read_only":
            to_replace = f"_{version}.json" if version else ".json"
            write_json(filename.replace(".csv", to_replace), read_csv(filename))
        elif operation == "delete_users":
            delete_users(read_json(filename), version)
        elif operation == "create_users":
            create_users(read_csv(filename), version)
