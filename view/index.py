#coding:utf-8

from _view import View
from random import choice
from config import connection
from time import time

URL_ENCODE = 'abcdefghijklmnopqrstuvwxyz0123456789'

def txt_by_url(url):
    url = url.lower()
    cursor = connection.cursor()
    cursor.execute('select txt from notepad where url=%s', url)
    txt = cursor.fetchone()
    if txt:
        txt = txt[0]
    else:
        txt = ''
    return txt

#@route("/xxxxx")
class ViewIndex(View):
    def get(self, url):
        if not url:
            while True:
                url = ''.join(choice(URL_ENCODE) for i in xrange(9))
                if not txt_by_url(url):
                    break
            self.redirect(url)
        else:
            self.render('/index.html', txt=txt_by_url(url), url=url)

    def post(self, url):
        if url:
            url = url.lower()
            txt = self.get_argument('txt', '').rstrip()
            now = time()
            cursor = connection.cursor()
            if txt:
                cursor.execute(
                    'insert into notepad (url,txt,`time`) values '
                    '(%s,%s,%s) ON DUPLICATE KEY UPDATE txt=%s,`time`=%s',
                    (url, txt, now, txt, now)
                )
            else:
                cursor.execute('delete from notepad where url=%s', url)
        self.finish({'time':now})