import requests as rq
from bs4 import BeautifulSoup as bs
from fake_useragent import UserAgent

ua = UserAgent()
headers = {"User-Agent": str(ua.chrome)}

search_url = "https://readallcomics.com/?story=babs&s=&type=comic"


def search_comics(query: str):
    response = rq.get(
        f"https://readallcomics.com/?story={query}&s=&type=comic", headers=headers
    )
    if response.status_code == 200:
        search_soup = bs(response.content, "lxml")
        comics_list = search_soup.find("ul", class_="list-story categories")
        comics = comics_list.find_all("a")
        results = [
            {"title": comic.get("title"), "link": comic.get("href")} for comic in comics
        ]
        return results


def scrape_comic_page(url):
    response = rq.get(url, headers=headers)
    if response.status_code == 200:
        search_soup = bs(response.content, "lxml")
        issues_list = search_soup.find("ul", class_="list-story")
        issues = issues_list.find_all("a")
        issues = [
            {"link": issue.get("href"), "title": issue.get("title")} for issue in issues
        ]
        issues.reverse()
        return issues


def scrape_issue_page(url):
    response = rq.get(url, headers=headers)
    if response.status_code == 200:
        soup = bs(response.content, "lxml")
        images = soup.find_all("img")
        for image in images[1:-1]:
            yield image.get("src")


if __name__ == "__main__":
    scrape_issue_page("https://readallcomics.com/x-babies-classic-tpb-part-2/")
