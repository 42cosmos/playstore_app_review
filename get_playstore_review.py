import argparse

import pandas as pd
from tqdm import tqdm
from google_play_scraper import reviews, Sort

from playstore_crawler import PlayStoreCrawler


def open_txt_file(file_path: str) -> list:
    with open(file_path) as f:
        data = f.read().strip().split("\n")
    return data


def score_into_sentiment(score: int) -> str:
    return ['negative', 'negative', 'neutral', 'positive', 'positive'][score - 1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", type=str, required=True, default='https://play.google.com/store/games')
    parser.add_argument("--file_path", type=str, required=True, default="./playstore_review.csv",
                        help="Path to save the collected game IDs. If not provided, the method will return the values.")
    parser.add_argument("--language", type=str, required=False, default="ko")
    parser.add_argument("--country", type=str, required=False, default="kr")
    args = parser.parse_args()

    crawler = PlayStoreCrawler()
    game_id_list = crawler.scroll_and_collect(args.url)
    print(f"Number of collected data: {len(game_id_list)}")
    crawler.quit_driver()

    all_review_list = []
    for game_id in tqdm(game_id_list):
        review_all, _ = reviews(
            game_id,
            lang=args.language,
            country=args.country,
            sort=Sort.NEWEST,
            count=1000,  # defaults to 100
            filter_score_with=None  # All score ( 1 ~ 5 )
        )

        all_review_list.extend(review_all)

    review_list = list(map(lambda x: [x["content"], x["score"]], set(all_review_list)))
    df = pd.DataFrame(review_list, columns=["txt", "score"])
    df.loc[:, "labels"] = df["score"].map(score_into_sentiment)
    print(df.shape)
    df.to_csv(args.file_path, index=False)
