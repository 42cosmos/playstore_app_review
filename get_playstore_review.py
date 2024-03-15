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
    url = 'https://play.google.com/store/games'

    crawler = PlayStoreCrawler()
    game_id_list = crawler.scroll_and_collect(url)
    print(f"Number of collected data: {len(collected_data)}")
    crawler.quit_driver()

    lang = 'ko'
    country = 'kr'

    all_review_list = []
    for game_id in tqdm(game_id_list):
        review_all, _ = reviews(
            game_id,
            lang=lang,
            country=country,
            sort=Sort.NEWEST,
            count=1000,  # defaults to 100
            filter_score_with=None # 모든 스코어 추출 ( 1 ~ 5 )
        )

        all_review_list.extend(review_all)

    review_list = list(map(lambda x: [x["content"], x["score"]], set(all_review_list)))
    df = pd.DataFrame(review_list, columns=["txt", "score"])
    df.loc[:, "labels"] = df["score"].map(score_into_sentiment)
    print(df.shape)
    df.to_csv("./playstore_review.csv", index=False)
