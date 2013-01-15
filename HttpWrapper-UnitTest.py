#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
from HttpWrapper import *

class HttpWrapperTestCase(unittest.TestCase):
    def setUp(self):
        self.h = HttpWrapper()
        #proxy info
        self.h.EnableProxyHandler({'http':'10.182.45.231:80','https':'10.182.45.231:80'})
        #auto direct 301,302... page
        self.h.EnableAutoRedirectHandler()
        #save cookie info between requests
        self.h.EnableCookieHandler()
        #enable gzip and deflate encoding, which will reduce transmite time
        self.h.EnableConetntEncodingHandler()

        #r = h.Request('image url')

        #h.RequestAsyc('http://www.baidu.com',data = {},header = {},callback = funcname )
        #h.RequestAsyc('http://www.sina.com.cn',callback = funcname )


        #h1 = HttpWrapper()
        #h1的设定应该不和h混淆


    def PageNotFind(self):
        r = self.h.Request('http://www.cnblogs.com/scottqiantest')
        assert r.code == 404
        #print r.GetContent().decode('utf-8').encode("GB18030") #encode to GB18030 for displaying in cmd window
        #print r.GetHeaderInfo()
        #with self.assertRaises(HttpWrapperException):
            #r.GetContent()

    def CorrectRequest(self):
        r = self.h.Request('http://www.cnblogs.com')
        assert r.code == 200

    def PostDataRequest(self):
        data = {'tbUserName'        : '1',
                'tbPassword'        : '1',
                '__EVENTTARGET'     : 'btnLogin',
                '__EVENTARGUMENT'   : '',
                '__VIEWSTATE'       : '/wEPDwULLTE1MzYzODg2NzZkGAEFHl9fQ29udHJvbHNSZXF1aXJlUG9zdEJhY2tLZXlfXxYBBQtjaGtSZW1lbWJlcm1QYDyKKI9af4b67Mzq2xFaL9Bt',
                '__EVENTVALIDATION' : '/wEWBQLWwpqPDQLyj/OQAgK3jsrkBALR55GJDgKC3IeGDE1m7t2mGlasoP1Hd9hLaFoI2G05'}
        r = self.h.Request('http://passport.cnblogs.com/login.aspx',data)
        assert r.content.decode('utf-8').find(u'用户不存在') > 0
    
    def RefererRequest(self):
        #tell server I'm from baidu.com
        headers = {'referer':'http://www.baidu.com'}
        r = self.h.Request('http://www.stardrifter.org/cgi-bin/ref.cgi',headers=headers)
        assert r.code == 200
        assert r.content.find(u'www.baidu.com') > 0

    def AutoRedirectRequest(self):
        #auto redirect is enabled by default in HttpWrapper
        r = self.h.Request('http://jigsaw.w3.org/HTTP/300/301.html')
        assert r.url == 'http://jigsaw.w3.org/HTTP/300/Overview.html'

        r = self.h.Request('http://jigsaw.w3.org/HTTP/300/302.html')
        assert r.url == 'http://jigsaw.w3.org/HTTP/300/Overview.html'

def suite():
    suite = unittest.TestSuite()
    suite.addTest(HttpWrapperTestCase('PageNotFind'))
    suite.addTest(HttpWrapperTestCase('CorrectRequest'))
    suite.addTest(HttpWrapperTestCase('PostDataRequest'))
    suite.addTest(HttpWrapperTestCase('RefererRequest'))
    suite.addTest(HttpWrapperTestCase('AutoRedirectRequest'))
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest = 'suite')
