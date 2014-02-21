from crawler import crawl_web, compute_ranks
from search import lucky_search, ordered_search

def test_engine():
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

test_engine()