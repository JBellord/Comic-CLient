#!/usr/bin/python3
from bs4 import BeautifulSoup as bs
from PIL import Image
import requests as rq
import dropbox
import os

# import webbrowser as wb

search_url = "https://readcomicsbook.net/ajax/search?q="
url = "https://readcomicsbook.net/comic/"
os.environ[
    "DROPBOX_KEY"
] = "sl.BnubEwJzQT9IWO1BaqXQxomsFvcrMAge16ianeLijLUXB0aUoQvCkipQzh-JxGCEK0H1fNNqw40UjuitRAyVL7Mfy4mgezry8p5kEANyl53aRF2VC_BG2TP8dzYOditIXbBsXFQm5ifpfo31b4mseFE"


def search(query: str):
    search_query = search_url + query
    response = rq.get(search_query)
    if response.status_code == 200:
        uuid = 1
        results = response.json()["data"]
        print(f"{results} Available Titles:")
        for i in results:
            print(f"({uuid}) Title: {i['title']}")
            uuid += 1
        return results
    else:
        return reponse.status_code


def get_comic_info(slug: str):
    response = rq.get(url + slug)
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        name = soup.find("h2").text
        chapters = soup.find("ul", class_="chapter-list")
        srcs = chapters.find_all("a")
        for src in srcs:
            yield {src.text: src["href"]}
    else:
        return response.status_code


def get_comic_issue(url: str):
    slug_url = url + "/all"
    response = rq.get(slug_url)
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        chapter = soup.find("div", class_="page-chapter")
        images = chapter.find_all("img")
        for i in images:
            yield i["src"]
    else:
        return response.status_code


def images_to_pdf(src_list, name):
    image_list = []
    for src in src_list:
        img = Image.open(rq.get(src, stream=True).raw)
        image = img.convert("RGB")
        image_list.append(image)
    image_list[0].save(
        f"/home/xavin/Documents/Projects/comics/{name}.pdf",
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=image_list[1:],
    )
    print("Download Finshed!")


def upload_comics(filename):
    dbx = dropbox.Dropbox(os.environ.get("DROPBOX_KEY"))
    with open(f"{filename}.pdf", "rb") as f:
        dbx.files_upload(
            f.read(),
            f"/comics/{filename}.pdf",
            mode=dropbox.files.WriteMode("overwrite"),
        )
