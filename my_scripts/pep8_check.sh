python3 -m venv venv
source venv/bin/activate
pip3 install flake8
pip3 install pep8-naming
pip3 install hacking
flake8 --exclude venv --statistics --max-line-length=120 --ignore=W503
deactivate
rm -rf venv
