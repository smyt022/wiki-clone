from django.shortcuts import render
from . import util
import markdown2 #use later to convert markdown->html
from markdown2 import Markdown

#will use this in entry_page function to convert
markdowner = Markdown()




#

def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries()
    })

def entry_page(request, entryTitle):
    try:
        if entryTitle=='usingSearchbar': #user is looking up an entry using the search bar
            return render(request,"encyclopedia/entryPage.html",{
            "md_entry": markdowner.convert(util.get_entry(title=request.GET['q'])),#same as next block except title is found in 'q' (searchbar input in layout.html template)
            "entry_title": request.GET['q']
        })
        return render(request,"encyclopedia/entryPage.html",{
        "md_entry": markdowner.convert(util.get_entry(title=entryTitle)),#get the entry with specified title, then convert markdown ->html
        "entry_title": entryTitle
        })
    except TypeError: #couldnt find page with specified title
        if entryTitle=='usingSearchbar': #user is looking up an entry using the search bar
            #see if searchbar query is a substring of another entry title found in the list of all entries. accumulate a list of entries that would work.
            searchQuery = request.GET['q']
            search_suggestions = [] #a list of wiki entries that have the query as a substring
            for entryName in util.list_entries():
                if searchQuery in entryName:#if it is a substring ->true
                    search_suggestions.append(entryName)
            #once all possible entries as checked for suggestions, render pagewith all suggestion (IF there are any)
            if len(search_suggestions) > 0:
                return render(request, "encyclopedia/index.html", {
                    "title": "Search results for: "+searchQuery,
                    "entries": search_suggestions
                })
        return render(request,"encyclopedia/entryPageNotFound.html") #if the encyclopedia entry was not found, there is a page for that to notify user




def entry_creation_page(request):
    return render(request,"encyclopedia/createNewEntry.html")