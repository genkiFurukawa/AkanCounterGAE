#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
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

import datetime
import os
import tweepy
import urlparse
import webapp2

consumer_key = '********'
consumer_secret = '********'

#開発環境かどうか
def is_dev():
    return os.environ["SERVER_SOFTWARE"].find("Development") != -1

TOP_URL = 'http://localhost:8080' if is_dev() else '********'
CALLBACK_URL = 'http://localhost:8080/callback' if is_dev() else '********'

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(
            """
            <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>Index</title>

                        <!-- Bootstrap -->
                        <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
                        <!-- Custom styles for this template -->
                        <link href="stylesheet/jumbotron-narrow.css" rel="stylesheet">

                        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
                        <!-- Include all compiled plugins (below), or include individual files as needed -->
                        <script src="bootstrap/js/bootstrap.min.js"></script>

                        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
                        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
                        <!--[if lt IE 9]>
                        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
                        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
                        <![endif]-->
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <ul class="nav nav-pills pull-right">
                                    <li class="active"><a href="http://twitter.com/#!/@8musa">Follow me, @8musa</a></li>
                                </ul>
                                <h3 class="text-muted">あかんカウンター</h3>
                            </div>

                            <div class="jumbotron">
                                <h1>あかんカウンター</h1>
                                    <p><a class="btn btn-lg btn-success" href="/auth" role="button">試してみる</a></p>
                                    <p class="lead">直近400ツイートから何回「あかん」というワードをつぶやいたかカウントします。
                                    ほんとは1000ツイートとかにしたいです...（APIの仕様のせい？）あと、スマホだと見にくい...</p>
                            </div>
                        </div>
                    </body>
                </html>
            """
        )

class AkanCounterAuth(webapp2.RequestHandler):
    def get(self):
        self.response.write("""
            <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>Auth</title>

                        <!-- Bootstrap -->
                        <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
                        <!-- Custom styles for this template -->
                        <link href="stylesheet/jumbotron-narrow.css" rel="stylesheet">

                        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
                        <!-- Include all compiled plugins (below), or include individual files as needed -->
                        <script src="bootstrap/js/bootstrap.min.js"></script>

                        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
                        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
                        <!--[if lt IE 9]>
                        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
                        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
                        <![endif]-->
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <ul class="nav nav-pills pull-right">
                                    <li class="active"><a href="http://twitter.com/#!/@8musa">Follow me, @8musa</a></li>
                                </ul>
                                <h3 class="text-muted">あかんカウンター</h3>
                            </div>
        """)
        try:
            auth = tweepy.OAuthHandler(consumer_key,consumer_secret,CALLBACK_URL)
            auth_url = auth.get_authorization_url()
            self.response.write('<div class="jumbotron">')
            self.response.write('<h1>あかんカウンター</h1>')
            self.response.write('<p><a class="btn btn-lg btn-success" href="%s" role="button">認証ページへ</a></p>' % auth_url)
            self.response.write('<p class="lead">Twitterの認証ページに飛びます</p>')
            self.response.write('</div>')
        except tweepy.TweepError:
            self.response.write('<p>ERROR! FAILED TO GET REQUEST TOKEN</p>')
        self.response.write('</div></body></html>')

class AkanCounterCallback(webapp2.RequestHandler):
    def get(self):
        #auth_tokenとauth_verifierを取得
        if 'QUERY_STRING' in os.environ:
            query = urlparse.parse_qs(os.environ['QUERY_STRING'])
        else:
            query = {}

        self.response.write(
            """
            <!DOCTYPE html>
                <html>
                    <head>
                        <meta charset="utf-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <title>Result</title>

                        <!-- Bootstrap -->
                        <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
                        <!-- Custom styles for this template -->
                        <link href="stylesheet/jumbotron-narrow.css" rel="stylesheet">

                        <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
                        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
                        <!-- Include all compiled plugins (below), or include individual files as needed -->
                        <script src="bootstrap/js/bootstrap.min.js"></script>

                        <!-- jQuery highlight.js-->
                        <script src="jsPlugin/jquery.highlight-4.js"></script>

                        <!-- HTML5 Shim and Respond.js IE8 support of HTML5 elements and media queries -->
                        <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
                        <!--[if lt IE 9]>
                        <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
                        <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
                        <![endif]-->

                        <style type="text/css">

                            .highlight {
                                background-color:yellow;
                            }

                        </style>

                        <script type="text/javascript">
                            function doHighLight(){
                                $('td').highlight('あかん');
                            }
                        </script>
                    </head>
            """
        )
        self.response.write('<body onLoad="doHighLight()">')
        self.response.write(
            """
            <div class="container">
                <div class="header">
                    <ul class="nav nav-pills pull-right">
            """)
        self.response.write('<li class="active"><a href="%s">Home</a></li>' % TOP_URL)
        self.response.write('<li class="active"><a href="http://twitter.com/#!/@8musa">Follow me, @8musa</a></li></ul>')
        self.response.write('<h3 class="text-muted">あかんカウンター</h3></div>')
        try:
            auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
            oauth_verifier = query['oauth_verifier'][0]
            oauth_token = query['oauth_token'][0]
            auth.set_request_token(oauth_token,oauth_verifier)
            auth.get_access_token(oauth_verifier)
            access_key = auth.access_token.key
            access_secret = auth.access_token.secret
            auth.set_access_token(access_key, access_secret)
            api = tweepy.API(auth)

            count=0
            html = ""
            for i in range(2):
                TL = api.user_timeline(page=i+1,count=200)
                for tweet in TL:
                    count += tweet.text.encode("utf-8").count("あかん")
                    if "あかん" in tweet.text.encode("utf-8"):
                        html += '<tr><td>%s</td><td>%s</td></tr>' % (tweet.text,tweet.created_at + datetime.timedelta(hours=9))
        except tweepy.TweepError:
            self.response.write('<p>ERROR! FAILED TO GET REQUEST TOKEN</p>')
        self.response.write('<h3>「あかん」というワードは直近400ツイート中%s回使いました</h3>' % str(count))
        self.response.write('<h3>「あかん」というワードが含まれるツイート</h3>')
        self.response.write('<table class="table table-striped table-bordered table-hover">')
        self.response.write("""
        <thead>
            <tr>
                <th>tweet</th>
                <th>date</th>
            </tr>
        </thead>
        <tbody>
        """)
        self.response.write(html)
        self.response.write('</tbody>')
        self.response.write('</div></body></html>')
        api.update_status("「あかん」というワードは直近400ツイート中%s回使いましたヾ(＠⌒ー⌒＠)ノ http://******** % str(count))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/auth', AkanCounterAuth),
    ('/callback', AkanCounterCallback)
], debug=True)