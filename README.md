# [RingCentral Engage Voice Python SDK](https://github.com/ringcentral/engage-voice-python)

[![Build Status](https://travis-ci.org/ringcentral/engage-voice-python.svg?branch=test)](https://travis-ci.org/ringcentral/engage-voice-python)
[![Coverage Status](https://coveralls.io/repos/github/ringcentral/engage-voice-python/badge.svg?branch=test)](https://coveralls.io/github/ringcentral/engage-voice-python?branch=test)

[API docs](https://engage-voice-api-docs.readthedocs.io/en/latest/).

## Installation

### PIP

```sh
pip3 install ringcentral_engage_voice
# or
pip install ringcentral_engage_voice
```

## Usage

```python
from ringcentral_engage_voice import RingCentralEngageVoice
# create from ringcentral app client id /secret
# you can create app from https://developer.ringcentral.com
ev = RingCentralEngageVoice(
  'RINGCENTRAL_CLIENT_ID',
  'RINGCENTRAL_CLIENT_SECRET'
)
# auth with password flow
ev.authorize(
  username = 'USERNAME',
  password = 'PASSWORD',
  extension = 'EXTENSION' # optional
)
# // can also auth with auth code flow
# // check https://developers.ringcentral.com/guide/authentication for more detail
ev.authorize(
  code = 'xxxx',
  redirectUri = 'yyyyyy'
)

# get access token, will expire in 5 minutes
token = ev.token['accessToken']

# // api request
# // check all api doc from https://engage-voice-api-docs.readthedocs.io/en/latest/
r = ev.get('/api/v1/admin/accounts')
assertEqual(len(r.json()) > 0, True)
```

For legacy server use:

```python
from ringcentral_engage_voice import RingCentralEngageVoice

# LEGACY_SERVER could be
# 'https://portal.vacd.biz',
# or  'https://portal.virtualacd.biz'
ev = RingCentralEngageVoice(
  server = process.env.LEGACY_SERVER
)

# only support username/password auth
await ev.authorize({
  username = process.env.LEGACY_USERNAME,
  password = process.env.LEGACY_PASSWORD
})

# api request
# check all api doc from https://engage-voice-api-docs.readthedocs.io/en/latest/
let r = ev.get('/api/v1/admin/accounts')
r = r.json()
expect(len(r) > 0).toBe(true)

```

## Instance methods

```python
ev._request(
    method,
    endpoint,
    params = None,
    json = None,
    data = None,
    files = None,
    multipart_mixed = False,
    headers = None
)

ev.get(endpoint, params = None)

ev.post(endpoint, json = None, params = None, data = None, files = None, multipart_mixed = False)

ev.put(endpoint, json = None, params = None, data = None, files = None, multipart_mixed = False)

ev.patch(endpoint, json = None, params = None, data = None, files = None, multipart_mixed = False)

ev.delete(endpoint, params = None)
```

## Virtual Environment

The venv module allows you to create a lightweight "virtual environment" within your own site directory, isolated from system site directories. The virtual environment has it's own Python binary and can have its own independent set of installed Python packages in its site directories. This is a good way to to create an isolated test environment to test out this code

## Test

To use the virtual environments, make sure you have pip3 and python3.6+ setup, then execute the following:

```bash
bin/init
source venv/bin/activate
pip install -r requirements.txt
cp env-sample.env .env
# edit .env fill all fields

# now test
./bin/test

# test non-lagecy API
python3 test/engage_voice_spec.py

# test lagecy API only
python3 test/engage_voice_lagecy_spec.py
```

To test without virtual environments and in your system directory, make sure you have pip3 and python3.6+, then execute the following:

```sh
pip3 install -r requirements-dev.txt
pip3 install -r requirements.txt
cp env-sample.env .env
# edit .env fill all

# now test
./bin/test
```

## Credits

Based on [Tyler](https://github.com/tylerlong)'s [https://github.com/tylerlong/ringcentral-python](https://github.com/tylerlong/ringcentral-python).

## License

MIT
