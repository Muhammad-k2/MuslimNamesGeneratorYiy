"""MuslimScrapper is dual web-scraper module to generate and search muslim names from 'SearchTruth' and 'MuslimNames' webserver, it uses HTML-Scrapping technique
to get data converts them as list and strings.
It can generate muslims names with meanings and translation from A-Z and can search names also with provided meaning. 

Features.
1.Search names with meanings for both gender.
2.Generate muslim names for both gender.
3.Has huge database with list from A-Z.
4.No 3rd party modules used.
5.Uses HTML scrapping to fetch data from two famous islamic websites.
6.Work with python3 and support for lower versions.
7.Name,meaning and translation for all names available.
8.Easy and efficient methods to fetch data from both websites.

@Note : All private methods starts from scraper_xxx_xxx() format, ex : scraper_fetch()

MuslimScrapper : V 1.0
Dated 25-05-2019
written by Haseeb mir (haseebmir.hm@gmail.com)  
"""

#Import URL and random modules.
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen 
import random

#Constants for URL.
SEARCH_TRUTH_URL = "https://www.searchtruth.com/baby_names/names.php?"
ST_MEANING_TABLE = '<td itemprop="description">'
ST_NAME_TABLE = '<td itemprop="name">'

#Constants for muslim names URL.
MUSLIM_NAME_URL = "https://www.muslimnames.info/"
MN_MEANING_TABLE = '<div class="name_row_mean">'
MN_TRANS_TABLE = '<div class="name_row_trns">'
MN_NAME_TABLE = "" #Dynamic Name table because had to append gender also.

"""================================================================
========================PUBLIC METHODS FOR SEARCH TRUTH============
==================================================================="""

"""INFO : 'SearchTruth' Method to search name with meaning.
ARGS : 
name - Name to search.
gender - Gender of name, provide "m" for Male and "f" for Female.
RETURN : name with meaning.
"""
def searchTruth_search(name,gender):
    if not name or not gender:
        return None
    search_url = SEARCH_TRUTH_URL + "name=" + name + "&ntype=" + gender + "&stype=sname&find=1"
    name = scraper_get_names_meanings(search_url)
    return name

"""INFO : 'SearchTruth' Method to generate list of muslim names.
ARGS : 
letter - Letter to generate list from, ex 'A','H','K'.
gender - Gender of name, provide "m" for Male and "f" for Female.
show_meaning - Show meanings with name, Defaults to false.
RETURN : name with meaning.
"""
def searchTruth_names(letter,gender,show_meaning=False):
    names_url = SEARCH_TRUTH_URL + "ntype=" + gender + "&find=2&letter=" + letter
    names_list = scraper_get_names_meanings(names_url) if show_meaning else scraper_get_names(names_url)
    return names_list 

"""INFO : 'SearchTruth' Method to generate random muslim names.
ARGS : limit - Number of names to generate,Defaults to 10.
show_meaning - Show meanings with name, Defaults to false.
RETURN : random names of size limit with random gender.
"""
def searchTruth_random(limit=10,show_meaning=False):
    letters = [chr(i) for i in range(ord('a'),ord('z')+1)]
    genders = ['m','f']

    letter,gender = random.choice(letters),random.choice(genders)

    names_url = SEARCH_TRUTH_URL + "ntype=" + gender + "&find=2&letter=" + letter
    names_list = scraper_get_names_meanings(names_url)[:limit*2] if show_meaning else scraper_get_names(names_url)[:limit]
    return names_list

"""================================================================
========================PUBLIC METHODS FOR MUSLIM NAMES============
==================================================================="""

"""INFO : 'MuslimNames' Method to search name with meaning.
ARGS : 
name - Name to search.
RETURN : name with meaning.
"""
def muslimNames_search(name):
    search_url = MUSLIM_NAME_URL + "search?name=" + name + "/"
    name = scraper_get_names_meanings(search_url)
    return name

"""INFO : 'MuslimNames' Method to generate list of muslim names.
ARGS : 
letter - Letter to generate list from, ex 'A','H','K'.
gender - Gender of name, provide "m" for Male and "f" for Female.
show_meaning - Show meanings with name, Defaults to false.
show_translation - Show translation with name, Defaults to false.
list_limit - Limit of names in list, Defaults to 3.
RETURN : name with meaning.
"""
def muslimNames_names(letter,gender,show_meaning=False,show_translation=False,list_limit=3):
    global MN_NAME_TABLE
    NAME_TABLE = '<div class="name_row_name '
    gender = "boys" if gender == "m" else "girls"
    MN_NAME_TABLE =	NAME_TABLE + gender + '">'
    names_list = []

    for index in range(1,list_limit+1):
    	names_url = MUSLIM_NAME_URL + "baby-" + gender + "/" + letter + "/" + "muslims-names-" + letter + "-" + str(index) + "/"
    	
    	if show_meaning:
        	names_list.append(scraper_get_names_meanings(names_url))
    	elif show_translation:
        	names_list.append(scraper_get_names_translation(names_url))    	
    	else:
    		names = scraper_get_names(names_url)
    		names_list.append(names)		
    return names_list 

"""INFO : 'MuslimNames' Method to generate random muslim names.
ARGS : limit - Number of names to generate, Defaults to 10.
show_meaning - Show meanings with name, Defaults to false.
RETURN : random names of size limit with random gender.
"""
def muslimNames_random(limit=10,show_meaning=False):
    global MN_NAME_TABLE
    NAME_TABLE = '<div class="name_row_name '
    letters = [chr(i) for i in range(ord('a'),ord('z')+1)]
    genders = ['boys','girls']
    names_list = []
    letter,gender = random.choice(letters),random.choice(genders)
    MN_NAME_TABLE =	NAME_TABLE + gender + '">'

    for index in range(1,limit+1):
        names_url = MUSLIM_NAME_URL + "baby-" + gender + "/" + letter + "/" + "muslims-names-" + letter + "-" + str(index) + "/"
        names_list += scraper_get_names_meanings(names_url) if show_meaning else scraper_get_names(names_url)

        if limit <= len(names_list):
        	names_list = names_list[:limit*2] if show_meaning else names_list[:limit]
        	break
    return names_list


"""========================================================
========================PRIVATE METHODS SECTION============
==========================================================="""

"""Private Method to get list of names from website using custom HTML scraper to parse data,
as there is no official API for this website so this is another neat way of getting data from website.""" 
def scraper_fetch(data,table_name):
    pos_list,names_list,meanings_list,names,tmp_data = [],[],[],[],[] 

    #If data is empty return Null.
    if not data:
        return None

    #Get positions of meanings.
    for index,value in enumerate(data):
        if data[index:index+(len(table_name))] == table_name:
            pos_list.append(index+len(table_name))
    
    #Get meaning data.    
    for pos in pos_list:
            while data[pos] != '<' or data[pos+1] != '/':
                name = data[pos]
                names.append(name)
                pos += 1    
    names_data = ""
    names_data = names_data.join(names)

    if table_name == ST_MEANING_TABLE or table_name == MN_MEANING_TABLE or  table_name == MN_TRANS_TABLE:
        meanings_list = names_data
        return meanings_list  

    #Get name positions.    
    pos_list.clear()
    for index,value in enumerate(names_data):
        if names_data[index:index+1] == ">":
            pos_list.append(index+1)

    #Get names data.        
    for pos in pos_list:
        while names_data[pos] != "<":
            if pos == len(names_data)-1:
                break
            name = names_data[pos]
            tmp_data.append(name)
            pos += 1
    names_data = ""                                
    names_list = names_data.join(tmp_data)
 
    return names_list     

#@Private method to get names with meanings.
def scraper_get_names_meanings(url):

	NAME_TABLE = ST_NAME_TABLE if "searchtruth" in url else MN_NAME_TABLE
	MEANING_TABLE = ST_MEANING_TABLE if "searchtruth" in url else MN_MEANING_TABLE

	data = scraper_read_url(url)
	names = scraper_fetch(data,NAME_TABLE)
	meanings = scraper_fetch(data,MEANING_TABLE)

	names_list,meanings_list = names.split("\n"),meanings.strip().split("\n")

	names_meanings_list = []
	#Trim white spaces from list.
	while(" " in meanings_list): 
		meanings_list.remove(" ")

	for index in range(len(names_list)):
		names_meanings_list.append(names_list[index].strip())
		names_meanings_list.append(meanings_list[index].strip())
	return names_meanings_list         

#@Private method to get names with meanings and translation.
def scraper_get_names_translation(url):
	data = scraper_read_url(url)
	names = scraper_fetch(data,MN_NAME_TABLE)
	trans = scraper_fetch(data,MN_TRANS_TABLE)
	names_list,trans_list = names.split("\n"),trans.strip().split("\n")

	names_trans_list = []

	for index in range(len(names_list)):
		names_trans_list.append(names_list[index].strip())
		names_trans_list.append(trans_list[index].strip())
	return names_trans_list  

#@Private method to get names.        
def scraper_get_names(url):
    NAME_TABLE = ST_NAME_TABLE if "searchtruth" in url else MN_NAME_TABLE
    data = scraper_read_url(url)
    names = scraper_fetch(data,NAME_TABLE).split()
    return names

#@Private method to read data from url.
def scraper_read_url(url):
    try: 
        response = urlopen(url)
        data = response.read().decode("UTF-8")
    except Exception as ex:
        print("Exception occured : ",ex)
    return data     

