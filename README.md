# playstore_app_review

scraping google play store app id and crawling reviews

## How to use

### 1. Install required packages
```bash
pip install -r requirements.txt
```

### 2. Google App ID scraping
You need "chromedriver" to use this code. You can download it from [here](https://googlechromelabs.github.io/chrome-for-testing/).
After download it, please put it in the same directory as the code.

If you want to collect only game id, you can use the following command. But pass this section when you want to collect
reviews.

```bash
python3 playstore_crawler.py --url {your_url} --file_path {file_path_without_extension}
```
Collected data won't save to a file if you don't specify the file path.
- filepath: Optional. The path to save the collected game IDs. If not provided, the method will return the values.
  - File path WITHOUT extection. The file will be saved as a txt file.

### 3. Review crawling
```bash
python3 get_playstore_review.py --url 'https://play.google.com/store/games' --file_path "./playstore_review.csv" --score_into_sentiment --headless
```

- **headless**: Optional. If True, the browser will be headless. Default is False
- **url**: Required. The URL of the Google Play Store page to scrape.
- **file_path**: Required. The path to save the collected game IDs. If not provided, the method will return the values.
  - File path WITH extection. The file will be saved as a ONLY csv file.
- **language**: Optional. The language of the reviews to scrape. Default is "ko".
- **country**: Optional. The country of the reviews to scrape. Default is "kr".
- **score_into_sentiment**: Optional. If True, the score will be converted into sentiment. Default is True
  - 1~2 -> Negative 
  - 3 -> Neutral
  - 4~5 -> Positive