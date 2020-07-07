from django.shortcuts import render, redirect
from . import util
import markdown
from django import forms
import re

class NewPage(forms.Form):
    title = forms.CharField(label="Page Title")
    entry = forms.CharField(widget=forms.Textarea)

class Edit(forms.Form):
    title = forms.CharField(label="Page Title")
    entry = forms.CharField(widget=forms.Textarea value="this")


def index(request, entries=util.list_entries()):
    hrefs = [f"wiki/{entry}" for entry in entries]
    entries_info = zip(entries, hrefs)
    return render(request, "encyclopedia/index.html", {
        "entries_info": entries_info,
    })

def title(request, title):
    
    # Retrieve the markdown format of the title
    md = util.get_entry(title)
    if not md:
        return render(request, "encyclopedia/error.html", {"msg": "Title not found"})

    entries = markdown.markdown(md)
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "entries": entries,
        })

def search(request):
    if request.method == "GET":
        return index(request)

    search = []
    form = request.POST
    search = form["search"]
    entries = util.list_entries()
    found = []

    # searched title is in wiki
    regex = r"\b"+f"{search}"+r"\b"
    r = re.compile(regex, re.IGNORECASE)
    found = list(filter(r.match, entries))
    if found:
        return redirect('title', title=found[0])

    # searched title partially matched entries
    r = re.compile(rf".*{search}.*", re.IGNORECASE)
    found = list(filter(r.match, entries))
    if found:
        return index(request, entries=found)

    return render(request, "encyclopedia/error.html", {"msg": "Title not found"})

def page_submission(request):
    """Page consisting of a form that the user can use to create a new page"""

    return render(request, "encyclopedia/page_submission.html", {
        "form": NewPage,
    })

def page_creation(request):
    if request.method == "GET":
        return render(request, "encyclopedia/error.html", {"msg": "Page cannot be accessed"})

    form = NewPage(request.POST)
    if form.is_valid():
        page_title = form.cleaned_data["title"]
        page_entry = form.cleaned_data["entry"]

    # check if page with same title exists
    r = re.compile(f"{page_title}", re.IGNORECASE)
    found = list(filter(r.match, util.list_entries()))

    if found:
        return render(request, "encyclopedia/error.html", {"msg": "Page exists"})

    # make the page
    with open(rf'entries/{page_title}.md', 'w') as file:
        file.write(page_entry)
        
    return redirect('title', title=page_title)
    
def edit(request, title):
    return render(request, "encyclopedia/edit.html", {
        "form": Edit
    })

def update(request):
    if request.method == "GET":
        return render(request, "encyclopedia/error.html", {"msg": "Page cannot be accessed"})

    form = Edit(request.POST)

    if form.is_valid:
        title = form.cleaned_data["title"]
        entry = form.cleaned_data["entry"]

    # edit the page
    with open(rf'entries/{title}.md', 'w') as file:
        file.write(page_entry)
    
    return redirect('title', title=title)


    
