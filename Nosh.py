from urllib2 import urlopen, HTTPError, URLError
from BeautifulSoup import BeautifulSoup
import re
from NetworkError import NetworkError


class Nosh(object):
    """ Simple interface to get data from Nosh.com """
    url_root = 'http://www.nosh.com/'
    cache = None

    def __init__(self, cache=False):
        if cache:
            import memcache
            self.cache = memcache.Client(['127.0.0.1:11211'], debug=0)

    def get_menu_items_from_url(self, url):
        soup = None
        if self.cache:
            soup = self.cache.get(url)
        if not soup:
            try:
                html = urlopen(url).read()
            except HTTPError, e:
                raise NetworkError(e, "HTTP Error %s" % e.code)
            except URLError, e:
                raise NetworkError(e, "URL Error")
            except:
                raise NetworkError("Network error")
            soup = BeautifulSoup(html)
            if self.cache:
                self.cache.set(url, soup)

        menu_items = {}
        links = soup.findAll('a', attrs={'href': re.compile('^/menuitem/*')})
        for link in links:
            text = link.findAll(text=True)
            if text:
                menu_items[text[0]] = self.url_root + link['href']

        return menu_items

    def get_item_description_from_url(self, url):
        soup = None
        if self.cache:
            soup = self.cache.get(str(url))
        if not soup:
            try:
                html = urlopen(url).read()
            except HTTPError, e:
                raise NetworkError(e, "HTTP Error %s" % e.code)
            except URLError, e:
                raise NetworkError(e, "Error %s" % e.code)
            except:
                raise NetworkError("Network error")
            soup = BeautifulSoup(html, fromEncoding="UTF-8")
            if self.cache:
                self.cache.set(str(url), soup)
        desc = soup.find('div', attrs={'class': 'ow-dtl-desc'})
        return desc.string.strip()
