# Cloud Computing Lab — Student Setup Guide

## Prerequisites

- A **GitHub account** — sign up at https://github.com/signup
- Your **AWS access keys** (Access Key ID + Secret Access Key) — provided by your instructor
- **Postman** installed — download at https://www.postman.com/downloads/
- The **course repository** link: https://github.com/sergiuvoicu/CloudComputingSummerSchool
- A **unique stage name** within the class — recommended: first 3 letters of your first
  name + first 3 letters of your last name (e.g. Sergiu Voicu → `servoi`)

---

## Step 1 — Add your AWS keys as Codespaces secrets

Do this **before** Step 2. Names must match exactly (uppercase).

1. Go to https://github.com/settings/codespaces
2. **Codespaces secrets** → **New secret**
   - Name: `AWS_ACCESS_KEY_ID`
   - Value: your Access Key ID provided
   - Repository access: search for and select **`sergiuvoicu/CloudComputingSummerSchool`**
   - **Add secret**
3. **New secret** again
   - Name: `AWS_SECRET_ACCESS_KEY`
   - Value: your Secret Access Key provided
   - Repository access: search for and select **`sergiuvoicu/CloudComputingSummerSchool`**
   - **Add secret**

---

## Step 2 — Create your codespace

1. Open https://github.com/sergiuvoicu/CloudComputingSummerSchool
2. **Code** → **Codespaces** tab → **Create codespace on main**

---

## Step 3 — Wait for setup (~5 minutes), then deploy

1. Wait until the terminal shows:
   - `✅ AWS credentials OK — account <number>, region eu-north-1`
   - `✅ Environment ready.`
2. If you don't see the banner, run:
   ```bash
   bash .devcontainer/post-create.sh
   ```
3. Deploy (replace `<your-stage>` with your stage name):
   ```bash
   ./node_modules/.bin/serverless deploy --stage <your-stage> --region eu-north-1 --config serverless.yml
   ```
4. Wait for the `endpoints:` section with your API URL.

---

## Closing your codespace

**Stop** (between sessions — keeps your files, frees compute):

- Bottom-left corner → click the codespace name → **Stop Current Codespace**
- Or go to https://github.com/codespaces, find your codespace, click the **`...`**
  (three-dot menu) on its right, then click **Stop codespace**

**Delete** (when finished — push your work to Git first):

- Go to https://github.com/codespaces, click the **`...`** (three-dot menu) next to your
  codespace, then click **Delete**

Stop between sessions. Delete only after you've pushed any work you want to keep.

---

## Step 4 Postman Setup

- On GitHub, open the repo's postman/ folder: https://github.com/sergiuvoicu/CloudComputingSummerSchool/tree/main/postman
- Click the collection file → on the file page click the Download raw file button (the download icon, top-right of the file view). Repeat for the environment file.
- In desktop Postman → Import (top-left) → drag in (or browse to) the two downloaded files → Import.
- Top-right environment dropdown → select the imported environment.
- Update the environment values as such:
    - Populate STAGE with the name you chose for your stack
    - To populate the API_ID, login to your AWS user, go to Search -> API Gateway -> Look for summerschool-<your-stack-name> -> take the corresponding ID
    ![alt text](images/api_id.png)
    - To populate the API_KEY, login to your AWS user, go to Search -> API Gateway -> API Keys (left side) -> Look for summerschool-<your-stack-name> -> take the corresponding ID
    ![alt text](images/api_key.png)
- Make sure you save the environment and you have it selected (top right). You can now send a request
    ![alt text](images/postman.png)

## Troubleshooting

| Symptom | Fix |
|---|---|
| No `✅ Environment ready` banner | Run `bash .devcontainer/post-create.sh` |
| ⚠️ AWS credentials warning | Re-check both secrets + repo access (Step 1), then press `Ctrl`/`Cmd`+`Shift`+`P`, type **Rebuild Container** in the search box, and click it |
| `python3.13` runtime warning on deploy | Ignore it |
| `{"message":"Forbidden"}` when testing | Add the `x-api-key` header with your API key (see note below) |
| Deploy permission errors | Contact your instructor |

**Finding your API key:** after deploying, the terminal prints an `api keys:` section like:

```
api keys:
  summerschool_servoi_apikey: <your-secret-key> - Key for servoi
```

When testing your endpoint in postman, add a header named `x-api-key` set to that `<your-secret-key>`
value.