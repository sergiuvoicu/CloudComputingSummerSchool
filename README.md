# Prerequisites
1. Install git https://git-scm.com/
2. Check installation by git --version in a terminal
3. Install Node https://nodejs.org/en
4. Check installation by node --version and npm --version
5. Install aws CLI https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
6. Check installation by aws --version
7. Install direnv https://direnv.net/docs/installation.html
8. Check installation by direnv --version
9. Install pyenv https://github.com/pyenv/pyenv
9. Install Postman

FOR WINDOWS - use WSL

1. Install WSL https://learn.microsoft.com/en-us/windows/wsl/install
2. Install distribution Ubuntu 20.4
3. Install the WSL extension for VSCode
4. Install git https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-git
5. Check installation by git --version in a terminal
6. Install Node through NVM https://learn.microsoft.com/en-us/windows/dev-environment/javascript/nodejs-on-wsl
    1. Install curl
    2. Execute curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash
    3. nvm install --lts
7. Check installation by node --version and npm --version
8. Install AWS CLI https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
    1. sudo apt install unzip
    2. curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    3. unzip awscliv2.zip
    4. sudo ./aws/install
9. Check installation by aws --version
10. Install direnv https://direnv.net/docs/installation.html
    1. curl -sfL https://direnv.net/install.sh | bash
    2. echo 'eval "$(direnv hook bash)' >> ~/.bashrc`
11. Check installation by direnv --version
12. Install pyenv https://github.com/pyenv/pyenv
    1. curl -fsSL https://pyenv.run | bash
    2. echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    3. echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    4. echo 'eval "$(pyenv init - bash)"' >> ~/.bashrc
    5. sudo apt-get update
    6. sudo apt-get upgrade
    7. sudo apt-get install build-essential
    8. pyenv install 3.10.4
    9. pyenv global 3.10.4
13. Check version by python --version

**Note: For Windows always check environment variables list in order for the CLIs to be recognised in the terminal**

# Setup
1. git clone https://github.com/sergiuvoicu/CloudComputingSummerSchool
2. npm install
3. Check installation by ./node_modules/.bin/serverless --version
4. Rename .envrc2 to .envrc
5. Run direnv allow in the terminal

Expected outcome:
```
direnv allow
direnv: loading ~/Documents/SummerSchoolCloudComputing/.envrc
direnv: export +AWS_DEFAULT_REGION +AWS_REGION +PROJ_STAGE +VIRTUAL_ENV +aws_account_id +environment ~PATH ~XPC_SERVICE_NAME
```
6. pip install -r dependencies/requirements.txt -t dependencies/python/lib/python3.11/site-packages
7. pip install -r requirements-dev.txt


