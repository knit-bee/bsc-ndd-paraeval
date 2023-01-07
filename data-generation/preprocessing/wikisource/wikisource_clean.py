"Remove unwanted sections from wikisource data"

import os

from lxml import etree


def remove_unwanted_sections(xml_tree):
    # remove tables and comments (trafilatura artefact)
    for element in xml_tree.iter(["comments", "table"]):
        element.getparent().remove(element)
    for element in xml_tree.iter("head"):
        if element.text is not None:
            if element.text.startswith("Anhang") or element.text.startswith(
                "Anmerkungen"
            ):
                for sibling in element.itersiblings():
                    element.getparent().remove(sibling)
                element.getparent().remove(element)
                break
    return xml_tree


def main():
    raw_dir = os.path.join("wikisource_maerchen", "raw")
    clean_dir = os.path.join("wikisource_maerchen", "clean")
    raw_files = os.listdir(raw_dir)
    for file in raw_files:
        file_path = os.path.join(raw_dir, file)
        doc = etree.parse(file_path)
        cleaned_doc = remove_unwanted_sections(doc)
        out_file_path = os.path.join(clean_dir, file)
        cleaned_doc.write(out_file_path, method="xml", encoding="utf8")


if __name__ == "__main__":
    main()
