import requests
from bs4 import BeautifulSoup as bs

search_url = "https://readcomiconline.li/AdvanceSearch?comicName="
og_url = "https://readcomiconline.li"

def search_comics(query: str):
    search_query = search_url + query
    response = requests.get(search_query)
    if response.status_code == 200:
        processed = bs(response.content, "html.parser")
        # print(processed)
        items = processed.find_all("div", class_="col cover")
        for item in items:
            item_img = item.find("img")
            item_a = item.find("a")
            title = item_img.get("title")
            href = item_a.get("href")
            data = {"title": title, "href": og_url + href}
            print(data)

if __name__== "__main__":
    search_comics("Overture")