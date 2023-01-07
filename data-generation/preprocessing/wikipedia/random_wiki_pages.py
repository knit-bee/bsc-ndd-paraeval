"Save article titles of 100 random Wikipedia articles to file"

import wikipedia


def random_wikipedia_pages(count):
    random_wiki_pages = []
    pages = wikipedia.random(count)
    for page in pages:
        if check_page_for_unwanted_conent(page):
            # no disambiguation site or list of stuff
            random_wiki_pages.append(page)
    while len(random_wiki_pages) < count:
        page = wikipedia.random(1)
        if check_page_for_unwanted_conent(page):
            random_wiki_pages.append(page)
    return random_wiki_pages


def check_page_for_unwanted_conent(page_title):
    if page_title.startswith("Liste"):
        return False
    try:
        wikipedia.page(page_title).summary
    except (wikipedia.exceptions.DisambiguationError, wikipedia.exceptions.PageError):
        return False
    return True


def main():
    wikipedia.set_lang("de")
    pages = random_wikipedia_pages(100)
    with open("wiki_articles.txt", "w", encoding="utf-8") as ptr:
        for page in pages:
            print(page, file=ptr)


if __name__ == "__main__":
    main()
