import requests
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

search_url = "https://readcomiconline.li/AdvanceSearch?comicName="
og_url = "https://readcomiconline.li"

ua = UserAgent()
headers = {'User-Agent': str(ua.chrome)}

driver = webdriver.Chrome(ChromeDriverManager().install())

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
            yield data

def scrape_comic_page(url: str):
    response = requests.get(f"{og_url}{url}")
    if response.status_code == 200:
        comic_page = bs(response.content, "lxml")
        items = comic_page.find_all("div", class_="col-1")
        links = [(item.find("a")).get("href") for item in items]
        links.reverse()
        print(links)

def scrape_comic_issue_page(url: str):
    response = requests.get(f"{og_url}{url}&s=s2", headers=headers)
    if response.status_code == 200:
        issue_page = bs(response.content, "lxml")
        file = open("test.html", "r+")
        file.write(str(issue_page))
        file.close()

if __name__== "__main__":
    # search_comics("Sandman")
    # scrape_comic_issue_page("/Comic/Die/Issue-1?id=145164")
    