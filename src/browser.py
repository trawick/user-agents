# Copyright 2014 Jeff Trawick, http://emptyhammock.com/
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import re


def msie_version(user_agent):
    m = re.search('MSIE ([0-9]+[\.0-9]*)', user_agent)
    if m:
        try:
            version = float(m.group(1))
        except ValueError:  # regex ensures that it is a floating point, but in case of range errors
            version = 4.0  # arbitrarily old and crufty (but maybe this isn't IE at all?)
        return version

    m = re.search('Mozilla/[0-9]\.0.*Trident/[0-9\.]+; .*rv:([0-9]+[\.0-9])', user_agent)
    if m:
        try:
            version = float(m.group(1))
        except ValueError:  # regex ensures that it is a floating point, but in case of range errors
            version = 11.0  # oldest version that has this format
        return version
    return None


def msie_and_older_than_version(user_agent, version):
    ver = msie_version(user_agent)
    if ver and ver < version:
        return True
    return False


class Browser(object):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def supports_server_name_indication(self):
        """
        References: http://en.wikipedia.org/wiki/Server_Name_Indication#Browsers_with_support_for_TLS_server_name_indication.5B10.5D
                    http://www.useragentstring.com/
                    http://blogs.msdn.com/b/kaushal/archive/2012/09/04/server-name-indication-sni-in-iis-8-windows-server-2012.aspx

        What supports SNI?  From Wikipedia:
        * IE >= 7, on Windows >= Vista
        ** What about on Macintosh?
        * Firefox 2.0 or later
        * Opera 8.0 or later if TLS 1.1 is enabled
        * Opera Mobile >= 10.1 on Android
        * Google Chrome -- relatively new versions on all platforms, some older versions on limited platforms
        * Safari >= 3.0 on OS X >= 10.5.6 or Windows >= Vista
        * Konqueror/KDE >= 4.7
        * Mobile Safari on iOS >= 4.0
        * Android browser on Android >= 3.0
        * BlackBerry 10 and BlackBerry Tablet OS browser
        * Windows Phone 7
        * MicroB on Maemo
        * Odyssey on MorphOS

        Note: Checks below do NOT match this list.
        """
        ver = msie_version(self.user_agent)
        if ver:
            if ver < 7.0:
                return False
            m = re.search('Windows NT ([0-9]+[\.0-9]*)', self.user_agent)
            if not m:
                if 'Macintosh' in self.user_agent:
                    return False  # no idea if this is true, so be conservative for now
                return True  # some future Windows version that we can't recognize?
            try:
                version = float(m.group(1))
            except ValueError:  # regex ensures that it is a floating point, but in case of range errors
                version = 99.0  # assume it is a future version that we can't recognize
            if version < 6.0:  # before Vista (XP, Windows Server 2003, older)?
                return False
            return True

        if 'Chrome/' in self.user_agent or 'Chromium/' in self.user_agent or ' CriOS/' in self.user_agent:
            return True

        if 'Firefox/' in self.user_agent and 'Seamonkey/' not in self.user_agent:
            return True

        if 'Safari/' in self.user_agent and 'Android' not in self.user_agent and 'Chrome' not in self.user_agent:
            if 'iPhone OS ' in self.user_agent:
                m = re.search('iPhone OS ([0-9])_', self.user_agent)
                if m:
                    if int(m.group(1)) < 4:
                        return False
            return True

        m = re.search('Android.*Opera Mobi/.* Version/([0-9]+[\.0-9][0-9]*)$', self.user_agent)
        if m:
            try:
                version = float(m.group(1))
            except ValueError:  # regex ensures that it is a floating point, but in case of range errors
                version = 99.0  # assume it is a future version that we can't recognize
            return version >= 10.1

        m = re.search('Android.*Opera Mini/.* Version/([0-9]+[\.0-9][0-9]*)$', self.user_agent)
        if m:
            try:
                version = float(m.group(1))
            except ValueError:  # regex ensures that it is a floating point, but in case of range errors
                version = 99.0  # assume it is a future version that we can't recognize
            return version >= 11.1  # I don't have any good information about support.  I tested this version myself.

        m = re.search(' Konqueror/([0-9]+[\.0-9]+)', self.user_agent)
        if m:
            try:
                version = float(m.group(1))
            except ValueError:  # regex ensures that it is a floating point, but in case of range errors
                version = 99.0  # assume it is a future version that we can't recognize
            return version >= 4.7

        return False  # We're white-listing; we may have missed an unpopular browser that really supports SNI


def self_test():
    ie8_string = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0)'
    ie11_string = 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko'
    tests = [(False, 'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; Sprint APA9292KT Build/GRJ90) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
             (True, 'Mozilla/5.0 (Linux; Android 4.4.4; Nexus 4 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.141 Mobile Safari/537.36'),
             (True, 'Mozilla/5.0 (iPod; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/35.0.1916.41 Mobile/11D257 Safari/9537.53'),
             (True, 'Mozilla/5.0 (iPod; CPU iPhone OS 6_1_6 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) CriOS/35.0.1916.38 Mobile/10B500 Safari/8536.25'),
             (True, 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.76.4 (KHTML, like Gecko) Version/6.1.4 Safari/537.76.4'),
             (True, ie8_string),
             (True, 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'),
             (True, 'Mozilla/5.0 (iPod touch; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53'),
             (True, 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:30.0) Gecko/20100101 Firefox/30.0'),
             (True, ie11_string),
             (True, 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36'),
             (True, 'Mozilla/5.0 (iPod; CPU iPhone OS 6_1_6 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B500 Safari/8536.25'),
             (True, 'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_2_1 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5'),
             (False, 'Mozilla/5.0 (iPod; U; CPU iPhone OS 3_1_3 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7E18 Safari/528.16'),
             (False, 'Mozilla/5.0 (Linux; U; Android 2.3.3; en-us; LS670 Build/GRI40) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1'),
             (False, 'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1; FDM; .NET CLR 1.1.4322)'),
             (True, 'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)'),
             (True, 'Opera/9.80 (Android 2.3.5; Linux; Opera Mobi/ADR-1309251116) Presto/2.11.355 Version/12.10'),
             (True, 'Opera/9.80 (Android; Opera Mini/7.5.35613/35.3226; U; en) Presto/2.8.119 Version/11.10'),
             (True, 'Mozilla/5.0 (X11; Linux) KHTML/4.9.1 (like Gecko) Konqueror/4.9'),
             (False, 'Mozilla/5.0 (compatible; Konqueror/3.5; Windows NT 6.0) KHTML/3.5.6 (like Gecko)'),
             ]

    for res, agent in tests:
        b = Browser(agent)
        assert res == b.supports_server_name_indication(), 'SNI capability of agent "%s" is not %s' % (agent, res)
    assert msie_and_older_than_version(ie8_string, 9.0)
    assert msie_and_older_than_version(ie8_string, 8.1)
    assert not msie_and_older_than_version(ie8_string, 8.0)
    assert msie_and_older_than_version(ie11_string, 11.1)
    assert not msie_and_older_than_version(ie11_string, 9.0)
    print 'User agent test cases successful...'


if __name__ == '__main__':
    self_test()
