import requests
import whois
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama


# I know it seems obvious, and it sort of seems stupid, but I'm going to explain which
# Libraries I imported and why.
# The first one is the requests library, to, you know, mak web requests and the like.
# Next is the urllib parse, urlparse, and urljoin. This is specifically to parse urls
# and join join parts of urls. Example, strippng www/http out and leaving only the base level TLD.
# or taking goo and then joining gle.com
# Beautiful Soup is literally exactly what it sounds like.
# colorama was so I could use the console color codes for when I output the data.
# This is for cmd/shell/terminal - call it whatever, but things like 0F 0A 0B 0C etc etc.
# ThenI imported whois because I thought I might try to be a _bit_ helpful and show you that I'm
# dead serious about this. I imported whois to grab relative info about the domain you are trying to scan.
# Just in case something interesting pops up in there somehow.

# I am blatantly following a tutorial, but using my own code format, variables,
# commentation for this, because I feel it will help me get a bit better with
# python. So, I want to make it explicit, I did not "come up with this". I found
# a tutorial on web request and link grabbing/enumeration and am using it to learn.

# init the colorama module
colorama.init()

GREEN = colorama.Fore.GREEN
WHITE = colorama.Fore.WHITE
RESET = colorama.Fore.RESET

# About to get us a shit ton of links, then, we will separate them between
# Internal anchors and external anchors. (that way we can just filter the
# bullshit and get straight to whether or not if this is a fake site or not )
internal_urls = set()
external_urls = set()
all_the_urls = set()

# This is literally just the number of URLS I could scrape from that website.
total_urls = 0 # was originally total_urls_visisted

# Clearly, I am looking to see if you have me a URL, or an IP or some bullshit.
# I am only looking to parse URLs to enumerate.
def is_valid(url):

    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def is_registered(domain_name):
    """
    A function that returns a boolean indicating
    whether a `domain_name` is registered
    """
    try:
        w = whois.whois(domain_name)
    except Exception:
        return False
    else:
        return bool(w.domain_name)


# This is where the bulk of the code comes in.
# Now I'm going to crawl the website I see (only 1 layer deep for now).
def get_all_website_links(url):

    # EVery URL found within the set you see, "urls".
    urls = set()

    # domain name of the URL without the protocol
    # This means http, www, ftp, sftp, etc etc. Just the TLD, google.com not www.google.com or http://google.com
    # We don't need any of that extra shit tbh.
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    # This might seem obvious to anyone who can read HTML or Python, but now I'm grabbing, or
    # rather scanning the website page and reading the HTML source directly.
    # Once I have the HTML, I look specifically for the anchor tags (e.g.: a href="")
    # Since we are crawling the website to find links, I am specifically parsing for a href tags.
    # However, this same code could I guess also be applied to parse for other tags in the HTML code
    # Such as ftp, emailto, phone, or some other tag you wanted to fuck with.

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)

        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
            # Now that we have confirmed this is NOT a blank URL or some BS URL
            # It's clear that if the link matches the TLD we are scanning this is likely an internal URL.
        if href in internal_urls:
            # already in the set
            continue
            # HOWEVER, if we find a domain that is NOT one we are crawling, we can reasonably assume this
            # This is a external URL and ergo, probably what we are looking for to be honest.
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{WHITE}[!!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        #print(f"{GREEN}[+] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)

    return urls

# Here you can see we are defining a function. The function to crawl, this is what will do the actual
# crawling. It will count the number of URLS/Links visited/crawled. However, JUST IN CASE, you happen to
# run into a website with like, 10k links or some shit, I have set a paramater in here to limit the number
# of crawls. Curently, it's set to 250. Because honestly, even 250 is too big, but meh, whatever. At the
# very least you won't have anymore than output of 250 links unless you edit that number to something higher.
def crawl(url, max_urls=50):
    global total_urls
    total_urls += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls > max_urls:
            break
        crawl(link, max_urls=max_urls)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Website Link Crawler")
    parser.add_argument("url", help="The URL to extract links from.")
    parser.add_argument("-m", "--max-urls", help="Number of max URLs to crawl, default is 200 and fucking fifty.", default=250, type=int)

    args = parser.parse_args()
    url = args.url
    max_urls = args.max_urls

    crawl(url, max_urls=max_urls)

# Now that I have crawled the page and found XX links, I wanted to separate them individually and them count
# them together, because honestly, I'm weird fucking guy, and I like numbers. I like data. Don't make fun of me.
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))

    domain_name = urlparse(url).netloc

    # Ok, at this point I have everything I need now. I'm going to use f.open, f.write, f.close
    # to open a file, write to the file, then cloe said file.
    # However, again, I'm a weird guy so everything is separated However, for giggles, I also did
    # add in something NOT in the tutorial (actually I've been doing that a good bit throughout this code
    with open(f"{domain_name}_internal_links.txt", "w") as f:
        for internal_link in internal_urls:
            print(internal_link.strip(), file=f)

    # save the external links to a file
    with open(f"{domain_name}_external_links.txt", "w") as f:
        for external_link in external_urls:
            print(external_link.strip(), file=f)
