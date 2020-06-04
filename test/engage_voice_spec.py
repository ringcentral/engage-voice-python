try:
  from dotenv import load_dotenv
  load_dotenv()
except:
  pass

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
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
    r = ev.get('/api/v1/admin/accounts')
    self.assertEqual(len(r.json()) > 0, True)

if __name__ == '__main__':
    unittest.main()