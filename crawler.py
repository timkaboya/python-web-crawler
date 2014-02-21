from bs4 import BeautifulSoup

def get_page(url):
   try:
       import urllib
       return urllib.urlopen(url).read()
   except:
        return ""

    
# returns list of all links in page. 
def get_all_links(page):
    soup = BeautifulSoup(page)
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links
 
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