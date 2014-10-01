# -*- coding: utf-8 -*-

import webapp2

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain; charset=utf-8'
        self.response.out.write('Tämä on kuvavarasto.')

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)


