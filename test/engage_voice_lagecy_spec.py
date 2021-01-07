try:
  from dotenv import load_dotenv
  load_dotenv()
except:
  pass

import sys, os
# import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
import unittest
from ringcentral_engage_voice import RingCentralEngageVoice



LEGACY_USERNAME = ''
LEGACY_PASSWORD = ''
LEGACY_SERVER = ''

try:
  LEGACY_USERNAME = os.environ['LEGACY_USERNAME']
  LEGACY_PASSWORD = os.environ['LEGACY_PASSWORD']
  LEGACY_SERVER = os.environ['LEGACY_SERVER']
except:
  pass

class TestLegacy(unittest.TestCase):

  def test_legacy(self):
    print('running basic test')
    ev = RingCentralEngageVoice(
      None,
      None,
      LEGACY_SERVER
    )
    ev.authorize(
      username = LEGACY_USERNAME,
      password = LEGACY_PASSWORD
    )
    r = ev.get('/api/v1/admin/accounts')
    rr = r.json()
    r1 = None
    try:
      r1 = ev.post('/api/vx/admin/accounts1')
    except Exception as e:
      x = str(e)
      self.assertEqual(
        '401' in x or '404' in x,
        True
      )
      print(e, 'eee')
    try:
      r1 = ev.patch('/api/vx/admin/accounts1')
    except Exception as e:
      x = str(e)
      self.assertEqual(
        '401' in x or '404' in x,
        True
      )
      print(e, 'eee')
    try:
      r1 = ev.put('/api/vx/admin/accounts1')
    except Exception as e:
      x = str(e)
      self.assertEqual(
        '401' in x or '404' in x,
        True
      )
      print(e, 'eee')
    try:
      r1 = ev.delete('/api/vx/admin/accounts1')
    except Exception as e:
      x = str(e)
      self.assertEqual(
        '401' in x or '404' in x,
        True
      )
      print(e, 'eee')
    # ev.revokeLegacyToken()
    self.assertEqual(len(rr) > 0, True)
    # print('============')
    # print('test 6 min if expire')
    # print('============')
    # time.sleep(60 * 6)
    # r = ev.get('/api/v1/admin/accounts')
    # rr = r.json()
    # self.assertEqual(len(rr) > 0, True)

if __name__ == '__main__':
    unittest.main()