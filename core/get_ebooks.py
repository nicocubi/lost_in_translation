# Nico 03 Dec 2020, use the gutenberg library (https://github.com/c-w/Gutenberg)
# to retrieve ebooks from the Gutemberg project
# NOTE: activate the gutemberg conda environment (yes with an 'm' this time)

import os, sys, re, requests, json

from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers

from gutenberg.query import get_etexts
from gutenberg.query import get_metadata

from gutenberg.acquire import get_metadata_cache

#----------------USER PARAMETERS

# You can provide the language you want (default spanish)
language= 'es'

url_gutemberg="http://www.gutenberg.org/browse/languages/"


#-----------------
if len(sys.argv)>2:
    userlang= sys.argv[2]
    if userlang.lower() in ('es', 'en', 'fr', 'de', 'ru'):   # add more languageslater
        language=userlang.lower()

# We will fetch ebook numbers from this page
url_gutemberg=url_gutemberg+language
bookRegExp= re.compile(r'\s+<li class="pgdbetext"><a href="/ebooks/(\d+)">')  # captures book numbers (5 digits)

metadataFields=('author', 'title', 'language','subject','rights')
#----------------


def parseBookNumbers(weburl=url_gutemberg):
    outList= []  # list of book ids
    r = requests.get(weburl)
    txt= r.text
    if txt:
        for l in txt.split('\n'):
            m= bookRegExp.match(l)
            if m:
                outList.append(int(m.group(1)))
    return set(outList)


def fetch_text(book_num:int):
    """Retrieve the entire text of an ebook"""
    text = strip_headers(load_etext(book_num)).strip()
    return text

def fetch_metadata(book_num:int):
    m=None

    # Create a dictionary to output the metadata
    outDic= {'id':book_num}

    # Now retrieve the metadata ijn this dict
    for mfield in metadataFields:
        try:
            
                m = get_metadata(mfield, book_num)  # prints frozenset([u'Moby Dick; Or, The Whale'])

        except Exception as e:
            print("Problem for metadata",mfield,"of entry",book_num)
            print(e)
            # print("\nPOPULATING THE CACHE")
            # # We have to populate the cache
            # cache = get_metadata_cache()
            # cache.populate()
            # m= get_metadata('title', book_num)
        else:
            outDic[mfield] = list(m)

    return outDic

#----------------
if __name__=='__main__':

    #t =fetch_text(book_num)
    #m=fetch_metadata(book_num)
    #print(m)

    txtDir=os.path.abspath("../data/txt")
    metaDataDir=os.path.abspath("../data/metadata")

    for d in (txtDir, metaDataDir):
        if not os.path.exists(d):
            print("Creating directory",d)
            os.makedirs(d)


    book_ids= parseBookNumbers()
    print("DONE: {:d} book_ids detected for language {:s}".format(len(book_ids),language))

    # Fetching the text of each book
    problem=[]
    problemm=[]
    c=0
    mc=0
    for bookid in book_ids:

        # Download txt
        if not os.path.exists(os.path.join(txtDir,str(bookid)+'.txt')):
            try:
                with open(os.path.join(txtDir,str(bookid)+'.txt'), 'w') as f:
                    print("Downloading book", bookid)
                    t =fetch_text(bookid)
                    if t:
                        f.write(t)
                        c +=1
            except Exception as e:
                print(e)
                problem.append(bookid)

        else:
            print("INFO", bookid, "already exists as txt, skipping")

        # Download metadata
        jsonOut=os.path.join(metaDataDir,str(bookid)+'.json')
        if not os.path.exists(jsonOut):
            try:
                # Dump the metadata in a json file
                print("Downloading metadata for book", bookid)
                d =fetch_metadata(bookid)
                print(d)
                with open(jsonOut,'w') as j:
                    json.dump(d,j)
                mc +=1
            except Exception as e:
                print(e)
                problemm.append(bookid)

        else:
            print("INFO: metadata file for", bookid, "already exists, skipping")

    print("INFO: done, download text, {:d} books andn{:d} metadata files in {}".format(c,mc,txtDir))
    if len(problem)>0:
        print("WARNING: problems detected for the following ids:")
        print(problem)
    if len(problemm)>0:
        print("WARNING: metadata absent for the following ids:")
        print(problemm)