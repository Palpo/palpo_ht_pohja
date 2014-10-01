# -*- coding: utf-8 -*-

import palpolib


def add_to_kuvapalvelu(img, kws):
    pass #TODO
    

def main(url):
    for img_url, kws in palpolib.imgsFromUrl(url).iteritems():
        print(img_url)
        for kw in kws:
            print("- %s" % kw)
        add_to_kuvapalvelu(img_url, kws)


if __name__=='__main__':
    import sys
    if len(sys.argv) != 2:
        print("Usage: %s <WEBSITE_URL>" % (sys.argv[0],))
        sys.exit(1)
    main(sys.argv[1])
