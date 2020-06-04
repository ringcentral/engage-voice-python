# Demo

```bash
# Create env file, then fill all fields
cp env-sample.env .env

pip3 install virtualenv
virtualenv venv --python=python3
source ./venv/bin/activate
pip install python-dotenv pydash pylint twine ringcentral_engage_voice
python test.py
```
