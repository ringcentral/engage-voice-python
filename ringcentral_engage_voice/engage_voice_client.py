import pydash as _
try:  # py3
    import urllib.parse as urlparse
except:  # pragma: no cover
    import urlparse
from requests import Request, Session
from ringcentral import SDK
import sys
import platform
from requests.utils import quote
# import json

version = 'dev'
try:
  with open("version", "r") as fh:
    version = fh.read()
except:
    pass

SERVER = 'https://engage.ringcentral.com'
LEGACY_SERVERS = [
  'https://portal.vacd.biz',
  'https://portal.virtualacd.biz'
]
RINGCENTRAL_SERVER = 'https://platform.ringcentral.com'

# from https://github.com/tylerlong/ringcentral-python/blob/master/ringcentral_client/rest_client.py
def pretty_print_POST(req): # pragma: no cover
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

class RingCentralEngageVoice(object):
    def __init__(
      self,
      clientId = '',
      clientSecret = '',
      server = SERVER,
      rcServer = RINGCENTRAL_SERVER,
      apiPrefix = 'voice'
    ):
        self.clientId = clientId
        self.clientSecret = clientSecret
        self.server = server
        self.apiPrefix = apiPrefix
        self._token = None
        self._timer = None
        self.auto_refresh = False
        if clientId != '':
          self.rc = SDK(clientId, clientSecret, rcServer)
        self.isLegacy = self.isLegacyServer(server)
        self.debug = False

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def refresh(self): # pragma: no cover
        self.getToken(
          self.token['refreshToken']
        )

    def isLegacyServer (self, server):
      return server in LEGACY_SERVERS

    def joinPath(self, path):
        if path.startswith('http'):
          return path
        v = urlparse.urlparse(self.server)
        p = v.path
        arr = [p, self.apiPrefix, path]
        if self.isLegacy:
          arr = [p, path]
        return urlparse.urljoin(
          self.server, "/".join(
            urlparse.quote_plus(part.strip("/"), safe="/") for part in arr
          )
        )

    def patchHeader(self, header = {}):
        user_agent_header = '{name} Python {major_lang_version}.{minor_lang_version} {platform}'.format(
            name = 'ringcentral/engage-voice',
            major_lang_version = sys.version_info[0],
            minor_lang_version = sys.version_info[1],
            platform = platform.platform(),
        )
        shareHeaders = {
            'Content-Type': 'application/json',
            'User-Agent': user_agent_header,
            'RC-User-Agent': user_agent_header,
            'X-User-Agent': user_agent_header,
        }
        authHeader = {}
        if self.isLegacy:
            authHeader = self._legacyHeader()
        else: # pragma: no cover
            authHeader = {
                'Authorization': self._autorization_header()
            }
        return _.assign(shareHeaders, authHeader, header or {})

    def _request(
        self,
        method,
        endpoint,
        params = None,
        json = None,
        data = None,
        files = None,
        multipart_mixed = False,
        headers = None
    ):
        url = self.joinPath(endpoint)
        newHeaders = self.patchHeader(headers)
        req = Request(method, url, params = params, data = data, json = json, files = files, headers = newHeaders)
        prepared = req.prepare()
        if multipart_mixed:
            prepared.headers['Content-Type'] = prepared.headers['Content-Type'].replace('multipart/form-data;', 'multipart/mixed;')
        if self.debug: # pragma: no cover
            pretty_print_POST(prepared)
        s = Session()
        r = s.send(prepared)
        try:
            r.raise_for_status()
        except:
            if 'expired' in r.text: # pragma: no cover
                self.refresh()
                newHeaders = self.patchHeader(headers)
                req = Request(method, url, params = params, data = data, json = json, files = files, headers = newHeaders)
                prepared = req.prepare()
                s = Session()
                r = s.send(prepared)
                try:
                    r.raise_for_status()
                except:
                  raise Exception('HTTP status code: {0}\n\n{1}'.format(r.status_code, r.text))
            else:
                raise Exception('HTTP status code: {0}\n\n{1}'.format(r.status_code, r.text))
        return r

    def authorize (self, **kwargs):
        if self.isLegacy:
            self.legacyAuthorize(**kwargs)
        else: # pragma: no cover
            plat = self.rc.platform()
            plat.login(**kwargs)
            self.getToken()

    def legacyAuthorize (self, **kwargs):
        self.getLegacyToken(**kwargs)

    def getLegacyToken (self, username = '', password = ''):
        url = f'{self.server}/api/v1/auth/login'
        body = f'username={quote(username)}&password={password}'
        res = self._request(
            'post',
            url,
            data = body,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        r = res.json()
        self.token = r

    # def revokeLegacyToken (self):
    #     if self._token is not None:
    #         token = self.token['authToken']
    #         self.delete(f'/api/v1/admin/token/{token}')

    def getToken (self, refreshToken = None): # pragma: no cover
        url = ''
        token = ''
        body = ''
        if refreshToken is None:
          url = f'{self.server}/api/auth/login/rc/accesstoken?includeRefresh=true'
          token = self.rc.platform().auth().data()['access_token']
          body = f'rcAccessToken={token}&rcTokenType=Bearer'
        else:
          url = f'{self.server}/api/auth/token/refresh'
          token = refreshToken
          body = f'refresh_token={token}&rcTokenType=Bearer'
        res = self._request(
            'post',
            url,
            data = body,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        )
        self.token = res.json()

    def _legacyHeader (self):
        accessToken = ''
        if self.token:
            accessToken = self.token['authToken']
        return {
            'X-Auth-Token': accessToken
        }

    def get(self, endpoint, params = None):
        return self._request('GET', endpoint, params)

    def post(self, endpoint, json = None, params = None, data = None, files = None, multipart_mixed = False):
        return self._request('POST', endpoint, params, json, data, files, multipart_mixed)

    def put(self, endpoint, json = None, params = None, data = None, files = None, multipart_mixed = False):
        return self._request('PUT', endpoint, params, json, data, files, multipart_mixed)

    def patch(self, endpoint, json = None, params = None, data = None, files = None, multipart_mixed = False):
        return self._request('PATCH', endpoint, params, json, data, files, multipart_mixed)

    def delete(self, endpoint, params = None):
        return self._request('DELETE', endpoint, params)

    def _autorization_header(self):
        if self.token:
            return 'Bearer {access_token}'.format(access_token = self.token['accessToken'])
        return 'Basic basic'