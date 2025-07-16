# Prerequisites
1. Install git https://git-scm.com/
2. Check installation by git --version in a terminal
3. Install Node https://nodejs.org/en
4. Check installation by node --version and npm --version
5. Install aws CLI https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
6. Check installation by aws --version
7. Install direnv https://gist.github.com/rmtuckerphx/4ace28c1605300462340ffa7b7001c6d
  1. For Windows you can use `winget direnv` after you install winget https://learn.microsoft.com/en-us/windows/package-manager/winget/
  2. Or you can follow the steps described above
  3. Or you can install WSL and install the packages using WSL https://learn.microsoft.com/en-us/windows/wsl/install
8. Check installation by direnv --version

** Note: For Windows always check environment variables list in order for the CLIs to be recognised in the terminal **

# Setup
1. git clone
2. npm install
3. Check installation by serverless --version
4. Rename .envrc2 to .envrc
5. Execute direnv allow

Expected outcome:
```
direnv allow
direnv: loading ~/Documents/SummerSchoolCloudComputing/.envrc
direnv: export +AWS_DEFAULT_REGION +AWS_REGION +PROJ_STAGE +VIRTUAL_ENV +aws_account_id +environment ~PATH ~XPC_SERVICE_NAME
```
6. pip install -r dependencies/requirements.txt -t dependencies/python/lib/python3.11/site-packages
7. pip install -r requirements-dev.txt
8. Check installation by python --version



