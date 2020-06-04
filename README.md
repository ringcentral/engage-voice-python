# [RingCentral Engage Voice API wrapper for Python](https://github.com/ringcentral/engage-voice-python)


[![Build Status](https://travis-ci.org/ringcentral/engage-voice-python.svg?branch=test)](https://travis-ci.org/ringcentral/engage-digital-python)

[API docs](https://engage-voice-api-docs.readthedocs.io/en/latest/).

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
  password = 'PASSWORD'
)
# // can also auth with auth code flow
# // check https://developers.ringcentral.com/guide/authentication for more detail
ev.authorize(
  code = 'xxxx',
  redirectUri = 'yyyyyy'
)
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

# revoke api token
ev.revokeLegacyToken()
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

## Test

```bash
bin/init
source venv/bin/activate
pip install -r requirements.txt
cp env-sample.env .env
# edit .env fill all fields
./bin/test
```

## Credits

Based on [Tyler](https://github.com/tylerlong)'s [https://github.com/tylerlong/ringcentral-python](https://github.com/tylerlong/ringcentral-python).

## License

MIT
