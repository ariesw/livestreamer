import os
import unittest

from livestreamer import Livestreamer, PluginError, NoPluginError
from livestreamer.plugins import Plugin
from livestreamer.stream import *

class TestPluginStream(unittest.TestCase):
    def setUp(self):
        self.session = Livestreamer()

    def assertDictHas(self, a, b):
        for key, value in a.items():
            self.assertEqual(b[key], value)

    def _test_akamaihd(self, surl, host, streamname):
        channel = self.session.resolve_url(surl)
        streams = channel.get_streams()

        self.assertTrue("live" in streams)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, AkamaiHDStream))
        self.assertEqual(stream.host, host)
        self.assertEqual(stream.streamname, streamname)

    def _test_hls(self, surl, url):
        channel = self.session.resolve_url(surl)
        streams = channel.get_streams()

        self.assertTrue("live" in streams)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, HLSStream))
        self.assertEqual(stream.url, url)

    def _test_rtmp(self, surl, url, params):
        channel = self.session.resolve_url(surl)
        streams = channel.get_streams()

        self.assertTrue("live" in streams)

        stream = streams["live"]
        self.assertTrue(isinstance(stream, RTMPStream))
        self.assertEqual(stream.params["rtmp"], url)
        self.assertDictHas(params, stream.params)

    def test_plugin(self):
        self._test_rtmp("rtmp://hostname.se/stream",
                         "rtmp://hostname.se/stream", dict())

        self._test_rtmp("rtmp://hostname.se/stream live=1 num=47",
                        "rtmp://hostname.se/stream", dict(live=True, num=47))

        self._test_rtmp("rtmp://hostname.se/stream live=1 qarg='a \'string' noq=test",
                        "rtmp://hostname.se/stream", dict(live=True, qarg='a \'string', noq="test"))

        self._test_hls("hls://http://hostname.se/playlist.m3u8",
                       "http://hostname.se/playlist.m3u8")

        self._test_akamaihd("akamaihd://http://hostname.se/stream",
                            "http://hostname.se", "stream")

if __name__ == "__main__":
    unittest.main()
