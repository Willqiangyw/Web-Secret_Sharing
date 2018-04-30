#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

# [START imports]
import os

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail, app_identity
import cloud_IO as algo
import metaDataModel

import os
import urllib

import googleapiclient
from googleapiclient import discovery

import jinja2
import webapp2

SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Send Email'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

class File(ndb.Model):

    filt_name = ndb.StringProperty(indexed=False)
    N_share = ndb.StringProperty(indexed=False)
    K_require = ndb.StringProperty(indexed=False)
    hash_value = ndb.StringProperty(indexed=False)





# [START main_page]
class MainPage(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('./template/main.html')
        self.response.write(template.render(template_values))
# [END main_page]

class Encrypt(webapp2.RequestHandler):
    def get(self):
        except_ = self.request.get('except', False)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'except' : except_
        }

        template = JINJA_ENVIRONMENT.get_template('./template/encrypt.html')
        self.response.write(template.render(template_values))

    def post(self):
        name = self.request.get('name')
        N_share = self.request.get('N_share')
        K_require = self.request.get('K_require')

        query_params = {
            'num' : N_share,
            'num_require' : K_require
        }
        self.redirect('/email?' + urllib.urlencode(query_params))


# [START guestbook]

# [END guestbook]
class Decrypt(webapp2.RequestHandler):

    def get(self):
        except_ = self.request.get('except', False)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'except' : except_
        }

        template = JINJA_ENVIRONMENT.get_template('./template/decrypt.html')
        self.response.write(template.render(template_values))

    def post(self):
 
        file = self.request.POST.getall('raw_file')
        name = self.request.get('name')
        email = self.request.get('email')

        # ******************************
        # add reconstruct algorithm here
        # ******************************
        decoder = algo.CombinedShare()  # Creat a new decoder object

        for f in file:
            sub_file = f.file.read()
            print("****************")
            # print(sub_file)

            decoder.addNewShare(sub_file)

        # After add all shares
        original_data, meta = decoder.decryptAndReconstruct()
        file_name = meta.fileName

        mail.send_mail(sender='{}@ece6102assignment4.appspotmail.com'.format(
        app_identity.get_application_id()),
                   to=email,
                   subject="Reconstructed file",
                   body="""
                        The reconstructed file is in the attachment!
                        """,
            attachments=[(file_name, original_data)])

        query_params = {
            'decrypt': True,
        }
        self.redirect('/success?' + urllib.urlencode(query_params))

class Success(webapp2.RequestHandler):

    def get(self):
        encrypt = self.request.get('encrypt', False)
        decrypt = self.request.get('decrypt', False)
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'decrypt' : decrypt,
            'encrypt' : encrypt
        }

        template = JINJA_ENVIRONMENT.get_template('./template/success.html')
        self.response.write(template.render(template_values))

class Email(webapp2.RequestHandler):

    def get(self):
        Nnum = int(self.request.get('num'))
        Knum_require = int(self.request.get('num_require'))

        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        lis = []
        for i in range(Nnum):
            lis.append(i + 1)


        print("****************************************")
        print(Nnum)
        print(Knum_require)
        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
            'lis' : lis,
            'num' : Nnum,
            'num_require' : Knum_require
        }

        template = JINJA_ENVIRONMENT.get_template('./template/email.html')
        self.response.write(template.render(template_values))

    def post(self):
        uploaded_file = self.request.POST.get('raw_file')   # uploaded_file is an file object
        content = uploaded_file.file.read()
        file_name = uploaded_file.filename
        print(file_name)
        num_N = int(self.request.POST.get('number'))
        num_K = int(self.request.POST.get('num_require'))

        print("****************************************")
        print(num_N)
        print(num_K)

        shares = algo.CombinedShare()
        allShares, meta = shares.DirectEncrypt(content, file_name, num_N, num_K)


        print("****************************************")

        email = self.request.POST.getall('email')

        for i in range(len(email)):
            share_name = str(file_name) + '_share_' + str(i + 1) + '.share'

            mail.send_mail(sender='{}@ece6102assignment4.appspotmail.com'.format(
                app_identity.get_application_id()),
                       to=email[i],
                       subject="Encrypted shareds",
                       body="""
                            The shares are in the attachment!
                            """,
                attachments=[(share_name, allShares[i])])



        query_params = {
            'encrypt': True,
        }
        self.redirect('/success?' + urllib.urlencode(query_params))


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/encrypt', Encrypt),
    ('/decrypt', Decrypt),
    ('/success', Success),
    ('/email', Email),
    ('/us', Us)
], debug=True)
# [END app]
