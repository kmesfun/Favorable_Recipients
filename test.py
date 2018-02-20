#python3
#test.py
#https://www.youtube.com/watch?v=6tNS--WetLI
#Goal: The goal of the challenge is to match customer's pickup requests with available non-profit recipients.
import unittest
import challenge

class TestDistanceMethod(unittest.TestCase):
    #Given a coordinate that is less than 5 miles away
    def testLessthan5miles(self):
        coordstart = (37.728912,-122.324225)
        coordend = (37.764859,-122.36167)
        result = challenge.LatitudetoMiles(coordstart,coordend)
        self.assertIsNot(result,5)
        self.assertTrue((5>result))

class TestTimeInterval(unittest.TestCase):
    def testInterval(self):
        interval = challenge.timeInterval("8-9PM")
        self.assertEqual(interval,['20:00', '20:01', '20:02', '20:03', '20:04', '20:05', '20:06', '20:07', '20:08', '20:09', '20:10', '20:11', '20:12', '20:13', '20:14', '20:15', '20:16', '20:17', '20:18', '20:19', '20:20', '20:21', '20:22', '20:23', '20:24', '20:25', '20:26', '20:27', '20:28', '20:29', '20:30', '20:31', '20:32', '20:33', '20:34', '20:35', '20:36', '20:37', '20:38', '20:39', '20:40', '20:41', '20:42', '20:43', '20:44', '20:45', '20:46', '20:47', '20:48', '20:49', '20:50', '20:51', '20:52', '20:53', '20:54', '20:55', '20:56', '20:57', '20:58', '20:59', '21:00'])


class TestStoreData(unittest.TestCase):
    def testPickupdate(self):
        pickup = challenge.readPickup()
        typing = type(pickup)
        self.assertEqual(str(typing),"<class 'collections.defaultdict'>")

class TestRestrictions(unittest.TestCase):
    def testcategorywithRestrictions(self):
        self.assertEqual(challenge.categorywRestrictions(5, 52), ['Raw Meat'])
        self.assertEqual(challenge.categorywRestrictions(5,48),['Raw Meat', 'Seafood'])
        self.assertEqual(challenge.categorywRestrictions(5,53), [])
        self.assertEqual(challenge.categorywRestrictions(5, 63), [])

class TestTime(unittest.TestCase):
    def testGetHour(self):
        self.assertEqual(challenge.getHour('2016-11-29T16:00:00-08:00'), "16:00")

class TestOneHourGap(unittest.TestCase):
   def testHour(self):
       self.assertFalse(challenge.OneHourGap("18:00:00",['20:00', '20:01', '20:02', '20:03', '20:04', '20:05', '20:06', '20:07', '20:08', '20:09', '20:10', '20:11', '20:12', '20:13', '20:14', '20:15', '20:16', '20:17', '20:18', '20:19', '20:20', '20:21', '20:22', '20:23', '20:24', '20:25', '20:26', '20:27', '20:28', '20:29', '20:30', '20:31', '20:32', '20:33', '20:34', '20:35', '20:36', '20:37', '20:38', '20:39', '20:40', '20:41', '20:42', '20:43', '20:44', '20:45', '20:46', '20:47', '20:48', '20:49', '20:50', '20:51', '20:52', '20:53', '20:54', '20:55', '20:56', '20:57', '20:58', '20:59', '21:00']))
       self.assertTrue(challenge.OneHourGap("19:20:00",['20:00', '20:01', '20:02', '20:03', '20:04', '20:05', '20:06', '20:07','20:08', '20:09', '20:10', '20:11', '20:12', '20:13', '20:14', '20:15','20:16', '20:17', '20:18', '20:19', '20:20']))
       self.assertFalse(challenge.OneHourGap("19:10:00", ['20:20']))

if __name__ == '__main__':
    unittest.main()
