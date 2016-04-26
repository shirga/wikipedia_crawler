# -*- coding: utf-8 -*-
"""
Created on Wed Feb  20 13:45:40 2016

@author: Shir Gaster


This code starts from a random article in Wikipedia, and each time, recursively, follows the first link 
in the body to the next article, till reaches Philosophy or enter a loop.
Then, it calculates the langth of the path.
This can be done repeatedly using a loop, in order to calculate the average length of that path.

Args:
    repeats = number of repeats the code should run (500, unless changed)
    specific_article = allows selecting specific artilce instead of a random
    
Returns as printed output:
    Histogram of the path lengths - TBD
    Average Path length
    % of articles that didn't lead to philosophy
    Running time

"""

import requests
import time
from BeautifulSoup import BeautifulSoup
import matplotlib.pyplot as plt



#%%
def checkIfInLoop(article, temp_dic):
    """
    Check if we already seen this article
    If we did we are in a loop
    """
    if article in temp_dic:
        return True
    else:
        temp_dic[article] = True
        return False
    

def removeBrackets(page):
    """ 
    Go over the page and remove everything that is inside 
    brackets = "(" ")", except brackets inside <a> <a>
    
    :param page: text with brackets
    :return the texk as a string without the brackets and everything inside the brackers 
    """ 
    page = str(page)
    new_page = ""
    b = 0 # count ()
    t = 0 # count <>
    for i in page:
        if (b < 1): #not inside()
            if (i == '<'):
                t += 1
            if (i == '>'):
                t -= 1
        if (t < 1): # not inside <>
            if (i == "("):
                b += 1
            elif (i == ")"):
                b -= 1
            elif (b < 1):
                new_page += i
        else: #inside <> take all
            new_page += i
    return new_page
    

def checkArticleMap(article, next_a, a_map):
    """
    To reduce time we will keep a map of articles that lead to philosophy.
    For every article we will have the distance from philosophy
    Every article will be first checked if it's in the map
    """
    if next_a in a_map:
        a_map[article] = a_map[next_a]+1
        return True
    else:
        return False

    
def checkLink(title):
    """
    Some article have an empty page
    """
    bad_titles = ["page does not exist","Help:"]
    for x in bad_titles:
        if x in title:
            return False
    return True
      
def getNext(article, a_map, temp_dic):
    """
    Find the first link in the article
    
    """
    url_base = "https://en.wikipedia.org/wiki/"      
    article.replace(' ', '_')
    r = requests.get(url_base+article)
    soup = BeautifulSoup(r.text)
    main_body = soup.find('div',id="mw-content-text")
    if (main_body == None):
        print article, "has no main body"
        return None
    find = 0
    next_artical = None
    for paragraph in main_body.findAll({'p','ul'},recursive=False):
        paragraph = BeautifulSoup(removeBrackets(str(paragraph)))
        for i in paragraph.findAll('a'):
            try: 
                next_artical = i['title']
                if checkLink(next_artical):
                    find = 1
                    break
            except:
                continue
        if find:
            break
    
    # check the link we found 
    if (next_artical == None):
        print article
        return None
    # uncomment the next line to see the articles leading from the random one to the last one
    #print next_artical 
    if checkArticleMap(article, next_artical,a_map):
        return a_map[article]
    elif checkIfInLoop(next_artical, temp_dic):
        return -1
    #return the distance to philosophy
    path = getNext(next_artical, a_map, temp_dic)
    if (path > 0):
        a_map[article] = path +1
        return path +1
    else: 
        return path


def getRandomArticle():
    """
    This function randomize an article on wikipedia
    
    :return: a random article name
    """
    wiki_random = "https://en.wikipedia.org/wiki/Special:Random"
    r = requests.get(wiki_random)
    return r.url[30:]

def plotResults(distance_list):
    plt.hist(distance_list)
    plt.title("Distances Histogram")
    plt.xlabel("Distance")
    plt.ylabel("Frequency")
    plt.show()


def main(repeats, specific_article = None):
    """
    The main function recieves as input the number of required runs, and might recieve a specific article as an input instead of a random articles 
    """
    start_time = time.time()
    article_map = {}
    article_map["Philosophy"] = 0 
    distance_list = []
    no_phi_count = 0
    i = 0
    while(i < repeats):
        if specific_article == None:
            article = getRandomArticle()
        else:
            article = specific_article
        print "new random article = ", article
        temp_dic = {}
        distance = getNext(article, article_map, temp_dic)
        print distance
        if (distance > 0):
            distance_list.append(distance)
            i += 1
        elif(distance == None):
            print "bad article"
        else:
            no_phi_count +=1
            i += 1

    end_time = time.time()
    plotResults(distance_list)
    print "From", repeats, "random repeats", len(distance_list), "lead to philosophy and", no_phi_count , " dosen't"
    print "Average distance is", sum(distance_list)/len(distance_list), "articles"
    print "Running time = ", end_time - start_time  
    return "## Finish Running ##"
    
    
if __name__ == "__main__":
    repeats = 500
    specific_article = None
    print "Starting the program with", repeats, "runs"
    print main(repeats, specific_article)
 