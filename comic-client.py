#!/usr/bin/python3

from lib import search, images_to_pdf, get_comic_info, get_comic_issue, upload_comics
import sys


def main():
    name = input("Enter comic name:  ")
    results = search(name)
    print("\n")
    selected = input("Enter Comic ID:  ")
    selected_comic = results[int(selected) - 1]
    print("These are the Issues:\n")
    issue_info = [x for x in get_comic_info(selected_comic["slug"])][::-1]
    x = 1
    for i in issue_info:
        print(f"({x}) {list(i.keys())[0]}")
        x += 1
    issue_no = int(input("\nEnter Issue ID:  "))
    selected_issue = issue_info[issue_no - 1]
    selected_issue_src = list(selected_issue.values())[0]
    filename = (
        str(selected_comic["slug"])
        + "-"
        + str(list(selected_issue.keys())[0]).lower().replace(" ", "-")
    )
    print("-----------------------------------------")
    print("Downloading, please wait")
    print("-----------------------------------------")
    images_to_pdf(get_comic_issue(selected_issue_src), filename)
    print("-----------------------------------------")
    print("Uploading, please wait")
    print("-----------------------------------------")
    upload_comics(filename=filename)
    print("Done!")


if __name__ == "__main__":
    main()
