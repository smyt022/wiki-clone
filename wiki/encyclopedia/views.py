from django.shortcuts import render
from . import util
import markdown2  # use later to convert markdown->html
from markdown2 import Markdown  # Markdown() is a function to convert stuff
from django import forms  # use to work with creating and taking information from forms
import random

# forms to add new entries
class newEntryForm(forms.Form):
    entryTitle = forms.CharField(label="entry title")
    entry = forms.CharField(widget=forms.Textarea, label="markdown entry")


#

def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "All Pages",
        "entries": util.list_entries()
    })


def entry_page(request, entryTitle):
    try:
        if entryTitle == 'usingSearchbar':  # user is looking up an entry using the search bar
            return render(request, "encyclopedia/entryPage.html", {
                # same as next block except title is found in 'q' (searchbar input in layout.html template)
                "md_entry": Markdown().convert(util.get_entry(title=request.GET['q'])),
                "entry_title": request.GET['q']
            })
        return render(request, "encyclopedia/entryPage.html", {
            # get the entry with specified title, then convert markdown ->html
            "md_entry": Markdown().convert(util.get_entry(title=entryTitle)),
            "entry_title": entryTitle
        })
    except TypeError:  # couldnt find page with specified title
        if entryTitle == 'usingSearchbar':  # user is looking up an entry using the search bar
            # see if searchbar query is a substring of another entry title found in the list of all entries. accumulate a list of entries that would work.
            searchQuery = request.GET['q']
            search_suggestions = []  # a list of wiki entries that have the query as a substring
            for entryName in util.list_entries():
                if searchQuery in entryName:  # if it is a substring ->true
                    search_suggestions.append(entryName)
            # once all possible entries as checked for suggestions, render pagewith all suggestion (IF there are any)
            if len(search_suggestions) > 0:
                return render(request, "encyclopedia/index.html", {
                    "title": "Search results for: "+searchQuery,
                    "entries": search_suggestions
                })
        # if the encyclopedia entry was not found, there is a page for that to notify user
        return render(request, "encyclopedia/entryPageNotFound.html")


def entry_creation_page(request):
    return render(request, "encyclopedia/createNewEntry.html", {
        "form": newEntryForm()
    })

def entry_editing_page(request, entryTitle):

    #initialized text
    initial_text = Markdown().convert(util.get_entry(title=entryTitle))
    initial_title = entryTitle

    #render
    return render(request, "encyclopedia/editEntry.html", {
        "form": newEntryForm(initial = {"entry": initial_text, "entryTitle": initial_title})
    })



def entry_mdFile_creation(request):
    # saving the form as a python variable
    form = newEntryForm(request.POST)
    if form.is_valid():  # if form inputs are valid
        # extracting data from form into python string variables
        entryTitle = form.cleaned_data["entryTitle"]
        entryMarkdown = form.cleaned_data["entry"]

        # check if entry title already exists (if so, error message)
        list_of_entries = util.list_entries()
        for existing_title in list_of_entries:
            if existing_title == entryTitle:
                return render(request, "encyclopedia/pageAlreadyExists.html")  # error message saying that the page already exists

        # create the entry's file
        util.save_entry(entryTitle, entryMarkdown)

        # directly renders the newly created page
        return render(request, "encyclopedia/entryPage.html", {
            # get the entry with specified title, then convert markdown ->html
            "md_entry": Markdown().convert(util.get_entry(title=entryTitle)),
            "entry_title": entryTitle
        })

    # if form is not valid
    return render(request, "encyclopedia/createNewEntry.html", {
        "form": newEntryForm()
    })  # go back to page u were at (creating entry markdown)


def entry_mdFile_edit(request):
    #saving the form as a python variable
    form = newEntryForm(request.POST)
    if form.is_valid():
        #assigning form data to python variables
        entryTitle = form.cleaned_data["entryTitle"]
        entryMarkdown = form.cleaned_data["entry"]

        # CHECK IF THE ENTRY EXISTS 
        list_of_entries = util.list_entries()
        for existing_title in list_of_entries:
            if existing_title == entryTitle:
                #update the entry
                util.save_entry(entryTitle, entryMarkdown)

                # directly renders the newly saved page
                return render(request, "encyclopedia/entryPage.html", {
                    # get the entry with specified title, then convert markdown ->html
                    "md_entry": Markdown().convert(util.get_entry(title=entryTitle)),
                    "entry_title": entryTitle
                })
            
        #at this point, entry does not exist    
        return render(request, "encyclopedia/pageDoesNotExist.html")  # error message saying that edited page does not exist
            
        

    
def random_entry(request):
    #get number of existing entries
    list_of_entries = util.list_entries()
    numOfEntries = len(list_of_entries)

    #generate random number 
    chosenEntry = random.randint(0,numOfEntries-1)

    #render that entry
    return entry_page(request, list_of_entries[chosenEntry])#calling another views function that does the job


