#returns list of urls in which keyword is listed
def lookup(index, keyword):
    if keyword in index:
        urls = []
        for url in index[keyword]:
            urls.append(url[0])
        return urls
    else:
        return None
        
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