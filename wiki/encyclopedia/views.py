from django.shortcuts import render
from . import util
import markdown2 #use later to convert markdown->html
from markdown2 import Markdown

#will use this in entry_page function to convert
markdowner = Markdown()

#

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, entryTitle):
    try:
        return render(request,"encyclopedia/entryPage.html",{
        "md_entry": markdowner.convert(util.get_entry(title=entryTitle)),#get the entry with specified title, then convert markdown ->html
        "entry_title": entryTitle
        })
    except TypeError:
        return render(request,"encyclopedia/entryPageNotFound.html") #if the encyclopedia entry was not found, there is a page for that to notify user
