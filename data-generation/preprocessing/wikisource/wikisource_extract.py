"Download 'Kinder- und Hausmärchen' from wikisource and save as xml"

import os

import trafilatura
from lxml import etree


def main():
    URL = "https://de.wikisource.org/wiki/Kinder-_und_Hausm%C3%A4rchen"
    downloaded = trafilatura.fetch_url(URL)
    main_page = trafilatura.extract(downloaded, include_links=True, output_format="xml")
    xml_page = etree.fromstring(main_page)
    overview_table = xml_page.find(".//table")
    for row in overview_table.iter("row"):
        cells = row.getchildren()
        if not cells or "role" in cells[0].attrib:
            continue
        title = ""
        for i, cell in enumerate(cells):
            child = cell.find("ref")
            if child is None:
                continue
            if i == 0:
                title = child.text
            else:
                link = child.attrib.get("target")
                text_url = f"https://de.wikisource.org{link}"
                text_download = trafilatura.fetch_url(text_url)
                content = trafilatura.extract(
                    text_download, output_format="xml", include_comments=False
                )
                if content:
                    with open(
                        os.path.join("wikisource", "raw", f"{title}_{i}.xml"), "w"
                    ) as ptr:
                        ptr.write(content)


if __name__ == "__main__":
    main()
