import csv

import os
import sys
import time
import json
import urllib.request, urllib.parse


if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs


f = open('out.txt', 'w')

def articles():
    results = []

    with open('sources.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            id = str(row['id'])

            

            print(city, city_results) 
            results.append(row['latitude'])
            results.append(row['longitude'])
            results.append(city_results)
            #results_humanreadable.append([city, city_results])

    txt_file.write(str(results))
    txt_file.close()

stop_count = 100

def create_query(city_name):
    q = webhose.Query()

    yesterday_ts = str(int(time.time() - 86400))

    city_name = quote_plus(city_name)
    q.body_text = city_name
    q.site_type = 'news'
    q.ts = yesterday_ts
    q.language = 'english'

    return q

def single_city(city_name):
    city_query = create_query(city_name)
    city_results = webhose.search(city_query)
    return city_results



if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs

# Lazy import of BeautifulSoup.
BeautifulSoup = None

# URL templates to make Google searches.
news_ext          = "q=%(query)s&tbm=nws&tbs=sbd:1,qdr:h" # last hour, sorted by date NOT RELEVANCE 

url_home          = "http://www.google.%(tld)s/"
url_search        = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&btnG=Google+Search&inurl=https"+news_ext
url_next_page     = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&start=%(start)d&inurl=https"+news_ext
url_search_num    = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&btnG=Google+Search&inurl=https"+news_ext
url_next_page_num = "http://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&num=%(num)d&start=%(start)d&inurl=https"+news_ext

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar.
def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.
    @type  url: str
    @param url: URL to retrieve.
    @rtype:  str
    @return: Web page retrieved for the given URL.
    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """
    request = Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    cookie_jar.add_cookie_header(request)
    response = urlopen(request)
    cookie_jar.extract_cookies(response, request)
    html = response.read()
    #soup = BeautifulSoup(html, 'html.parser')
    #print (soup.prettify())
    #f.write(str(soup.prettify()))

    '''
    results = json.loads(response.read().decode("utf8"))
    data = results['responseData']
    print('Total results: %s' % data['cursor']['estimatedResultCount'])
    '''
    response.close()
    cookie_jar.save()
    return html

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.
def filter_result(link):
    try:

        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]

            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link

    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None

# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', num=100, start=0, stop=None, pause=2.0,
           only_standard=False):
    """
    Search the given query string using Google.
    @type  query: str
    @param query: Query string. Must NOT be url-encoded.
    @type  tld: str
    @param tld: Top level domain.
    @type  lang: str
    @param lang: Languaje.
    @type  num: int
    @param num: Number of results per page.
    @type  start: int
    @param start: First result to retrieve.
    @type  stop: int
    @param stop: Last result to retrieve.
        Use C{None} to keep searching forever.
    @type  pause: float
    @param pause: Lapse to wait between HTTP requests.
    @type  only_standard: bool
    @param only_standard: If C{True}, only returns the standard results from
        each page. If C{False}, it returns every possible link from each page,
        except for those that point back to Google itself. Defaults to C{False}
        for backwards compatibility with older versions of this module.
    @rtype:  generator
    @return: Generator (iterator) that yields found URLs. If the C{stop}
        parameter is C{None} the iterator will loop forever.
    """

    # Try to use BeautifulSoup 4 if available, fall back to 3 otherwise.
    global BeautifulSoup
    if BeautifulSoup is None:
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup

    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    hashes = set()

    # Prepare the search string.
    query = quote_plus(query)

    # Grab the cookie from the home page.
    get_page(url_home % vars())

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or start < stop:

        # Sleep between requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url)

        # Parse the response and process every anchored URL.
        soup = BeautifulSoup(html)
        anchors = soup.find(id='search').findAll('a')
        for a in anchors:

            # Leave only the "standard" results if requested.
            # Otherwise grab all possible links.
            if only_standard and (
                        not a.parent or a.parent.name.lower() != "h3"):
                continue

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                continue
            hashes.add(h)

            # Yield the result.
            yield link

        # End if there are no more results.
        if not soup.find(id='nav'):
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()

# When run as a script...
if __name__ == "__main__":

    from optparse import OptionParser, IndentedHelpFormatter

    class BannerHelpFormatter(IndentedHelpFormatter):
        "Just a small tweak to optparse to be able to print a banner."
        def __init__(self, banner, *argv, **argd):
            self.banner = banner
            IndentedHelpFormatter.__init__(self, *argv, **argd)
        def format_usage(self, usage):
            msg = IndentedHelpFormatter.format_usage(self, usage)
            return '%s\n%s' % (self.banner, msg)

    # Parse the command line arguments.
    formatter = BannerHelpFormatter(
        "Python script to use the Google search engine\n"
    )
    parser = OptionParser(formatter=formatter)
    parser.set_usage("%prog [options] query")
    parser.add_option("--tld", metavar="TLD", type="string", default="com",
                      help="top level domain to use [default: com]")
    parser.add_option("--lang", metavar="LANGUAGE", type="string", default="en",
                      help="produce results in the given language [default: en]")
    parser.add_option("--num", metavar="NUMBER", type="int", default=10,
                      help="number of results per page [default: 10]")
    parser.add_option("--start", metavar="NUMBER", type="int", default=0,
                      help="first result to retrieve [default: 0]")
    parser.add_option("--stop", metavar="NUMBER", type="int", default=0,
                      help="last result to retrieve [default: unlimited]")
    parser.add_option("--pause", metavar="SECONDS", type="float", default=2.0,
                      help="pause between HTTP requests [default: 2.0]")
    parser.add_option("--all", dest="only_standard",
                      action="store_false", default=True,
                      help="grab all possible links from result pages")
    (options, args) = parser.parse_args()
    query = ' '.join(args)
    if not query:
        parser.print_help()
        sys.exit(2)
    params = [(k,v) for (k,v) in options.__dict__.items() if not k.startswith('_')]
    params = dict(params)

    # Run the query.

    #querylst = []