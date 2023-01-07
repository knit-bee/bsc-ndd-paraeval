"Download revision history of Wikipedia articles"

import os
import sys

import wikipedia_histories


def main(file_with_article_list, output_dir):
    with open(file_with_article_list, "r", encoding="utf-8") as ptr:
        articles = [line.strip() for line in ptr.readlines()]

    for page_title in articles:
        page_data = wikipedia_histories.get_history(
            page_title,
            domain="de.wikipedia.org",
            include_text=True,
            output="split",
        )
        df = wikipedia_histories.to_df(page_data)
        page_title = page_title.replace("/", "-")
        output_file = os.path.join(output_dir, f"{page_title}.csv")
        os.makedirs(output_dir, exist_ok=True)
        df.to_csv(output_file)


if __name__ == "__main__":
    input_file, output_dir = sys.argv[1:]
    main(input_file, output_dir)
