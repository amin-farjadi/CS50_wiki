from django.shortcuts import render

from . import util

import markdown


def index(request):
    entries = util.list_entries()
    hrefs = [f"wiki/{entry}" for entry in entries]
    entries_info = zip(entries, hrefs)
    return render(request, "encyclopedia/index.html", {
        "entries_info": entries_info
    })

def title(request, title):
    
    # Retrieve the markdown format of the title
    md = util.get_entry(title)
    if not md:
        return render(request, "encyclopedia/error.html", {"msg": "Title not found"})

    entries = markdown.markdown(md)
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "entries": entries
        })

