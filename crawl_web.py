#returns the page contents in string from given url
def get_page(url):
   try:
       import urllib
       return urllib.urlopen(url).read()
   except:
        return ""

#returns the next url in page and it's end position
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote+1:end_quote]
    return url, end_quote
    
# returns list of all links in page. 
def get_all_links(page):
    links = []
    while True :
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            return links


# prints list separated by space
def print_list (list):
    for e in list:
        print e, list[e]

# returns list of all links linking to seed
def crawl_web(seed): 
    tocrawl = set([seed])
    crawled = set()
    index = {}
    graph = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
	    outlinks = get_all_links(content)
	    graph[page] = outlinks
            tocrawl.update(outlinks)
            crawled.add(page)             
    return index, graph 
 
# adds keyword to index if it's not in index, or else it just adds url to url_list
#  that is assoc to keyword    
def add_to_index(index, keyword, url):
    # format: index: [[keyword, [[url1, count], [url2, count]]]
    if keyword in index:
        if url not in index[keyword][0]:
            index[keyword].append([url, 1])
        else:
            for url_pair in index[keyword]:
                if url_pair[0] == url:
                    url_pair[1] = url_pair[1] + 1
        
    else:
        index[keyword] = [[url, 1]]

def record_user_click(index,keyword,url):
    urls = lookup (index, keyword)
    if urls:
        for entry in urls:
            if entry[0] == url:
                entry[1] = entry[1] + 1
                
#returns list of urls in which keyword is listed
def lookup(index, keyword):
    if keyword in index:
        urls = []
        for url in index[keyword]:
            urls.append(url[0])
        return urls
    else:
        return None

def split_string(source,splitlist):
    words = [ ]
    atsplit = True #At a split point
    for char in source:
        if char in splitlist:   #iterate through string one by one
            atsplit = True
        else:
            if atsplit:
                words.append(char)
                atsplit = False
            else:
                #adding char to last word: Building word one by one. *Not Appending
                words[-1] = words[-1] + char
    return words

def add_page_to_index (index, url, content):
    words = split_string(content, " ,.?!;:'[]{}()<>\/")
    for word in words:
        add_to_index(index, word, url)
    #update index to include all of the word occurences found in
    # the page content by adding the url to the assoc url list
    
def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    ranks = {}
    npages = len(graph)
    for page in graph:
	ranks[page] = 1.0 / npages
    for i in range(0, numloops):
	newranks = {}
	for page in graph:
	    newrank = (1 - d) / npages
	    # update by summing in the inlink ranks. 
            for node in graph:
		if page in graph[node]:
		    newrank = newrank + d * (ranks[node] / len(graph[node]))
	
	    newranks[page] = newrank
        ranks = newranks
    
    return ranks

def lucky_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    if not pages:
        return None
    best_page = pages[0]
    for candidate in pages:
        if ranks[candidate] > ranks[best_page]:
            best_page = candidate
    
    return best_page

def ordered_search(index, ranks, keyword):
    pages = lookup(index, keyword)
    return qsort(pages, ranks)

def qsort(pages, ranks):
    if not pages or len(pages) <= 1:
        return pages
    else:
        pivot = ranks[pages[0]]
        worse = []
        better = []
        for page in pages[1:]:
            if page <= pivot:
                worse.append(page)
            else:
                better.append(page)
        return qsort(worse, ranks) + [pages[0]] + qsort(better, ranks)
   
# start with tocrawl = [seed]
# crawled = []
# while there are no more pages tocrawl:
#    pick a page from tocrawl
#    check if we already crawled page:
#       add that page to crawled
#       add all the link targets on this page to tocrawl
#    return crawled

#links = get_all_links(get_page('http://xkcd.com/353'))
#print_list(links)

#crawled = crawl_web('http://www.udacity.com/cs101x/index.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#record_user_click(crawled, 'good', 'http://www.udacity.com/cs101x/crawling.html')
#print_list(crawled)

index, graph = crawl_web('http://www.udacity.com/cs101x/index.html')
ranks = compute_ranks(graph)
#print index
print "_+_+_+_++_+_++_+_+_+_+_++_+_+_++"
print lucky_search(index, ranks, 'walking')
#>>> https://www.udacity.com/cs101x/index.html

print lucky_search(index, ranks, 'kicking')
#>>> https://www.udacity.com/cs101x/crawling.html

print lucky_search(index, ranks, 'Ossifrage')
#>>> https://www.udacity.com/cs101x/flying.html

print lucky_search(index, ranks, 'ossifrage')
#>>> None

print "_+_+_+_++_+_++_+_+_+_+_++_+_+_++"
print ordered_search(index, ranks, 'to')
#>>> https://www.udacity.com/cs101x/index.html

print ordered_search(index, ranks, 'Ossifrage')
#>>> https://www.udacity.com/cs101x/flying.html

print ordered_search(index, ranks, 'crawl')
#>>> index crawling

print ordered_search(index, ranks, 'ossifrage')
#>>> None