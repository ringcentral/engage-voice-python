try:
  from dotenv import load_dotenv
  load_dotenv()
except:
  pass

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
import time
from ringcentral_engage_voice import RingCentralEngageVoice

RINGCENTRAL_CLIENTID = ''
RINGCENTRAL_CLIENTSECRET = ''

RINGCENTRAL_USERNAME = ''
RINGCENTRAL_PASSWORD = ''
RINGCENTRAL_EXTENSION = ''

try:
  RINGCENTRAL_CLIENTID = os.environ['RINGCENTRAL_CLIENTID']
  RINGCENTRAL_CLIENTSECRET = os.environ['RINGCENTRAL_CLIENTSECRET']

  RINGCENTRAL_USERNAME = os.environ['RINGCENTRAL_USERNAME']
  RINGCENTRAL_PASSWORD = os.environ['RINGCENTRAL_PASSWORD']
  RINGCENTRAL_EXTENSION = os.environ['RINGCENTRAL_EXTENSION']
except:
  pass

class TestEngageVoice(unittest.TestCase):

  def test_engage_voice(self):
    print('running basic test')
    ev = RingCentralEngageVoice(
      RINGCENTRAL_CLIENTID,
      RINGCENTRAL_CLIENTSECRET
    )
    ev.authorize(
      username = RINGCENTRAL_USERNAME,
      password = RINGCENTRAL_PASSWORD,
      extension = RINGCENTRAL_EXTENSION
    )
    # ev.debug = True
    # print('before')
    # print(ev.token)
    print('this will take 6 minutes to verify token expire')
    ev.refresh()
    # print('after')
    # print(ev.token)
    time.sleep(60 * 6)
    r = ev.get('/api/v1/admin/accounts')
    self.assertEqual(len(r.json()) > 0, True)

if __name__ == '__main__':
    unittest.main()