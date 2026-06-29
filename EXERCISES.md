# Cloud Computing Lab - Exercises

You'll extend **your own stack** (your stage). Everything you create is named with your
stage, so it never collides with anyone else's.

## Before you start

- Work in your codespace, deploy with your stage:
  ```bash
  ./node_modules/.bin/serverless deploy --stage <your-stage> --region eu-north-1 --config serverless.yml
  ```
- Every endpoint is private - send the `x-api-key` header (your key is in the deploy
  output under `api keys:`).
- Clean up when done: `serverless remove --stage <your-stage> --region eu-north-1 --config serverless.yml`

**Naming conventions** (use these everywhere):

| Thing             | Pattern                                              | Example (stage `virchi`)              |
| ----------------- | ---------------------------------------------------- | ------------------------------------- |
| Function          | `${self:service}_${self:provider.stage}_<name>`      | `summerschool_virchi_upsert-customer` |
| Table             | `${self:service}_${self:provider.stage}_<name>`      | `summerschool_virchi_customers`       |
| Bucket            | `${self:service}-${self:provider.stage}`             | `summerschool-virchi` (note: hyphen)  |
| Per-function role | `${self:service}_${self:provider.stage}_role_<name>` | `summerschool_virchi_role_...`        |

---

## Exercise 1 - Deploy the Upsert Customer function

**Goal:** get `POST /upsert-customer` working so it stores a customer in your DynamoDB table.

**Already written for you:** the handler (`services/lambda_upsert_customer.py`), the function
definition (`serverless_templates/Lambda.yml` → `UpsertCustomerFunction`), the table
(`serverless_templates/CustomersTable.yml`), and its IAM (`iam/CustomersTableIAM.yml`).

**Your task:** wire these into `serverless.yml`. There are two commented placeholders marking
where things go - one in the `functions:` block, one in `resources:`.

**Hints:**

- Look at how `ServerlessDeploymentBucket` is already pulled into `resources:` with the
  `${file(path):Key}` syntax. The same pattern links the function and the table.
- A function that writes to a table won't work if the table isn't part of your stack - so
  this exercise needs **both** placeholders filled, not just the function one.

**Done when:** the deploy succeeds, and a request like this returns success:

```bash
curl -X POST -H "x-api-key: YOUR_KEY" -H "Content-Type: application/json" \
  -d '{"firstName":"Ada","lastName":"Lovelace","email":"ada@example.com"}' \
  https://YOUR_ENDPOINT/upsert-customer
```

The table needs both `firstName` and `lastName` (they're the key), so always include them.
Confirm the item appears in your `summerschool_<stage>_customers` table.

---

## Exercise 2 - Deploy the Generate Report function

**Goal:** `GET /generate-report` scans your customers, writes a CSV, and uploads it to your S3 bucket.

**Already written for you:** the handler (`services/lambda_generate_report.py`), the function
(`serverless_templates/Lambda.yml` → `GenerateReportFunction`), the bucket
(`serverless_templates/S3.yml` → `SummerSchoolS3Bucket` + `SummerSchoolS3BucketPolicy`), and
its IAM (`iam/S3BucketIAM.yml`).

**Your task:** link the function and the **bucket resources** (bucket + bucket policy) into
`serverless.yml`, same pattern as Exercise 1.

**Hints:**

- The report is written to your bucket `summerschool-<stage>` under the prefix
  `SummerSchool/Reports/`. Without the bucket linked, the function has nowhere to upload.
- Make sure you've added at least one customer (Exercise 1) first - an empty table returns
  "No customer found!".

**Done when:** the deploy succeeds, `GET /generate-report` (with your key) returns success,
and a CSV appears in `s3://summerschool-<stage>/SummerSchool/Reports/`.

---

## Exercise 3 - Bonus (advanced): react to new reports

> For anyone who wants to go further. This is open-ended - the hints get you there, but you
> do the design.

**Goal:** whenever Generate Report drops a new CSV into S3, **automatically** record metadata
about that report in a new DynamoDB table - no API call, it just happens.

**Build three things:**

1. **A new table** `summerschool_<stage>_reports_metadata` (`PAY_PER_REQUEST`), with a sensible
   key - e.g. partition key `report_key` (the S3 object key, type String). Follow the pattern in
   `serverless_templates/CustomersTable.yml`.
2. **A new Lambda** (`summerschool_<stage>_report-metadata`) with a new handler file
   (e.g. `services/lambda_report_metadata.py`), triggered by an **S3 event** when an object is
   created in your reports bucket under `SummerSchool/Reports/` with suffix `.csv`.
3. On each trigger, **write a metadata item** to the new table: at minimum the object key, the
   bucket, the size in bytes, and the creation time.

**Hints:**

- **Terminology:** The mechanism is **S3 Event Notifications**; in Serverless Framework that's an `s3` event on your function. Filter it by
  `prefix: SummerSchool/Reports/` and `suffix: .csv` so it only fires on real reports.
- **Your bucket already exists in the stack.** A plain `s3` event tries to _create_ the bucket
  and will clash with `SummerSchoolS3Bucket`. Investigate the `existing: true` option on the
  event - it attaches the trigger to a bucket your stack already owns.
- You **don't need to download the file** - the S3 event payload already contains the bucket,
  object key, size, and event time.
- The `environment` variable (= `summerschool_<stage>_`) is available to every function, so in
  your handler you can do
  `dynamodb.resource("dynamodb").Table(os.environ["environment"] + "reports_metadata")`.

**Permissions you'll need to think about:**

- _Runtime:_ your new function's role needs `dynamodb:PutItem` on the new table. Follow the
  `iam/` snippet pattern - create `iam/ReportsMetadataIAM.yml` and attach it via
  `iamRoleStatements`, exactly like the other functions do.
- _Deployment:_ configuring an S3 notification means your **AWS keys** need permission to set
  the bucket's notification (`s3:PutBucketNotification`), and the `existing: true` path creates a
  small helper resource that needs IAM/Lambda permissions too. If your deploy fails with an
  `AccessDenied` mentioning bucket notifications, that's a credential limit, not your code -
  tell your instructor.

**Done when:** you call `GET /generate-report`, a CSV lands in S3, and within a few seconds a
matching item appears in `summerschool_<stage>_reports_metadata` with that report's key, size,
and timestamp. (Check the new function's **CloudWatch logs** to debug the trigger.)

---

## On permissions (short version)

There are two separate permission layers, and it's worth knowing which is which when something
fails:

- **Execution permissions** - what each _function's role_ is allowed to do at runtime (read a
  table, write to S3). You control these with the `iam/*.yml` snippets attached per function.
- **Deployment permissions** - what _your AWS keys_ are allowed to create. Exercises 1–2 need
  rights to create DynamoDB tables, S3 buckets, IAM roles, Lambdas, API Gateway, and
  CloudFormation stacks. Exercise 3 additionally needs S3 bucket-notification rights.

If a deploy stops with `AccessDenied`, it's almost always the deployment layer (your keys) -
contact your instructor rather than changing your code.
