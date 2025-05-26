from django.shortcuts import render, redirect

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "The requested entry was not found."
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })

def search(request):
    query = request.GET.get("q", "").strip()
    if not query: 
        return redirect("index")
    
    entries = util.list_entries()
    
    # Check for exact match (case-insensitive)
    for entry in entries:
        if query.lower() == entry.lower():
            return redirect("entry", title=entry)  # Use correct case

    # Find partial matches (substring)
    filtered_entries = [entry for entry in entries if query.lower() in entry.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": filtered_entries
    })
