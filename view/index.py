#coding:utf-8

import _env
import time
import urllib
import json
import tornado.web
import tornado.auth
from _view import View, LoginView, login, logout
from model.index import gen_url, txt_save, txt_by_url
from model.account import account_new
from model.history import history_get, history_count
from config import HOST
from lib.page import page_limit_offset
from _route import route

@route('/\:')
class History(LoginView):
    def get(self):
        self.render('/history.html')

@route('/\:logout')
class History(LoginView):
    def get(self):
        logout(self)
        self.redirect('/')

#@route('/api/(.*)')
#class ScriptApi(View):
#    def get(self,url=1):
#        from server import application
#        handlers = application.handlers[0]
#        print handlers
#        self.finish(repr(list(zip(handlers,list(i.pattern for i in handlers)))))


@route('/\:api/(.*)')
class ScriptApi(View):
    def get(self, url=''):
        if not url:
            self.finish('..hi.')
        else:
            self.finish(txt_by_url(url))

    def post(self, url=''):
        if not url:
            url = gen_url()
        txt = self.get_argument('txt', '').rstrip()
        txt_save(self.user_id, url, txt)
        self.finish('http://%s/%s' % (HOST, url))
        
@route('/\:signin')
class SignIndex(View):
    def get(self):
        self.render('/signin.html')

@route('/\:oauth')
class GoogleHandler(tornado.web.RequestHandler, tornado.auth.GoogleMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("openid.mode", None):
            user = self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        ax_attrs=["name", "email", "language", "username"]
        callback_uri = self.request.uri
        args = self._openid_args(callback_uri, ax_attrs=ax_attrs)
        self.redirect(self._OPENID_ENDPOINT + "?hl=zh-CN&" + urllib.urlencode(args))

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        else:
            name = user['name']
            email = user['email']
            user_id = account_new(name, email)
            login(self, user_id)
            self.redirect('/')

@route('/\:j/history')
@route('/\:j/history-(\d+)')
class J_History(LoginView):
    def get(self, n=1):
        #[timestamp,content, url , count ]
        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        user_id = self.user_id
        count = history_count(user_id)
        page , limit , offset = page_limit_offset(
            '/history-%s',
            count,
            n,
            15
        )
        _history = history_get(user_id, offset, limit)
        self.finish(json.dumps(_history + [[count, int(n), limit]]))
        

@route('/(.*)')
class Index(View):
    def get(self, url):
#        return self.finish(self.request.path)
        if not url:
            url = gen_url()
            self.redirect(url)
        else:
            self.render('/index.html', txt=txt_by_url(url), url=url)

    def post(self, url):
        if url:
            txt = self.get_argument('txt', '').rstrip()
            txt_save(self.user_id, url, txt)
        self.finish({'time':int(time.time())})
