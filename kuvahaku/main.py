# -*- coding: utf-8 -*-

import os
import webapp2
import jinja2
import logging

# Käytetään jinja2-sivupohjamoottoria.
# http://jinja.pocoo.org/docs/dev/
# Muutakin saa kyllä halutessaan käyttää...
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class IndexHandler(webapp2.RequestHandler):
    
    def get(self):
        
        search_keyword = self.request.get('q')
        
        # TODO: Hae kuvien tiedot Kuvavarastosta
        
        # Jotain placeholder-dataa...
        related_keywords = [u'lemmikki', u'kissa']
        images = [{'id': 'kuva_yx',
                   'original_url': 'http://www.cs.tut.fi/~palpo/materiaali/cat.jpg',
                   'thumbnail_url': 'http://storage.googleapis.com/palpoapp.appspot.com/kuva1',
                   'keywords': [u'eläin', u'harmaa', u'kissa']},
                  {'id': 'kuva_kax',
                   'original_url': 'http://www.cs.tut.fi/~palpo/materiaali/dog.jpg',
                   'thumbnail_url': 'http://storage.googleapis.com/palpoapp.appspot.com/kuva2',
                   'keywords': [u'eläin', u'iloinen', u'koira']},]
        template_values = {
            'related_keywords': related_keywords,
            'search_keyword': search_keyword,
            'images': images
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


class UpdateFormHandler(webapp2.RequestHandler):

    def post(self, image):

        # Avainsana-checkboxien id on muotoa keyword:<avainsana>
        KEYWORD_PREFIX = "keyword:"
 
        keywords = []
        for key, val in self.request.POST.iteritems():
            if key.startswith(KEYWORD_PREFIX):
                keywords.append(key[len(KEYWORD_PREFIX):])
            if key=='newkeyword' and val:
                keywords.append(val)
        
        logging.info("Kuvan %s uudet avainsanat:" % (image,))
        for kw in keywords:
            logging.info(kw)
            
        # TODO: Tallenna avainsanat Kuvavarastoon
        
        # Ohjataan takaisin hakuun josta tultiin.
        search_keyword = self.request.get('search_keyword')
        return self.redirect('/?q='+search_keyword)
    
    
class DeleteFormHandler(webapp2.RequestHandler):

    def post(self, image):
        logging.info("Poistetaan kuva %s..." % (image,))
            
        # TODO: Poista kuva
        
        # Ohjataan takaisin hakuun josta tultiin.
        search_keyword = self.request.get('search_keyword')
        return self.redirect('/?q='+search_keyword)
        

app = webapp2.WSGIApplication([
        ('/', IndexHandler),
        ('/update/(\w+)', UpdateFormHandler),
        ('/delete/(\w+)', DeleteFormHandler)], debug=True)

