from django.shortcuts import render, redirect
import markdown2
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def convert_md_to_html(title):
    md_text = util.get_entry(title)
    if md_text == None:
        return None
    else:
        html_output = markdown2.markdown(md_text)
        return html_output


def entries(request, title):
    content = convert_md_to_html(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
            "message": "This page is not exist!"
        })
    else:
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": content
        })


def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        content = convert_md_to_html(query)
        if content != None:
            return render(request, "encyclopedia/entries.html", {
                "title": query,
                "content": content
            })
        else:
            allentries = util.list_entries()
            if query != '':
                recom = []
                for entry in allentries:
                    if query.lower() in entry.lower():
                        recom.append(entry)
                return render(request, "encyclopedia/search.html", {
                    "recom": recom,
                    "query": query
                })
            else:
                return redirect("index")


def new(request):
    if request.method == "POST":
        title = request.POST["title"]
        n_cont = request.POST["text"]
        if title not in util.list_entries():
            util.save_entry(title, n_cont)
            content = convert_md_to_html(title)
            return render(request, "encyclopedia/entries.html", {
                "title": title,
                "content": content
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "This page is already exist!"
            })

    return render(request, "encyclopedia/new.html")


def edit(request):
    title = request.POST["title"]
    md_text = util.get_entry(title)
    return render(request, "encyclopedia/s_edit.html", {
        "title": title,
        "md_text": md_text
    })


def s_edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        n_cont = request.POST["text"]
        util.save_entry(title, n_cont)
        content = convert_md_to_html(title)
        return render(request, "encyclopedia/entries.html", {
            "title": title,
            "content": content
        })


def rand(request):
    entries = util.list_entries()
    rand = random.choice(entries)
    content = convert_md_to_html(rand)
    return render(request, "encyclopedia/entries.html", {
        "title": rand,
        "content": content
    })
