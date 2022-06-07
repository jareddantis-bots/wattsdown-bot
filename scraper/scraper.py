from PIL import Image
from requests import get
from scraper.ocr import ocr_cropped
from typing import Optional
import snscrape.modules.twitter as sntwitter
import pandas as pd


# Search strings for the Twitter API
MERALCO_SEARCH_STR = 'ADVISORY: from:meralco -filter:replies'

# Number of tweets to scrape per user
NUM_TWEETS = 25


class WattsdownScraper:
    def __init__(self):
        self.meralco_twt = sntwitter.TwitterSearchScraper(MERALCO_SEARCH_STR)
        self._meralco_df: Optional[pd.DataFrame] = None
        self._meralco_info = pd.DataFrame(columns=[
            'Tweet ID',
            'Username',
            'Outage Area',
            'Outage Date',
            'Outage Time',
            'Affected Areas'
        ])
    
    @property
    def meralco_outages(self) -> pd.DataFrame:
        return self._meralco_info
    
    def scrape_meralco_outages(self):
        scraped_tweets = []

        for i, tweet in enumerate(self.meralco_twt.get_items()):
            if i == NUM_TWEETS:
                break

            # Check if the tweet has an attached image
            tweet_image = None
            if len(tweet.media) > 0:
                tweet_image = tweet.media[0].fullUrl
            
            scraped_tweets.append([
                tweet.date,
                tweet.id,
                tweet.user.username,
                tweet.content,
                tweet_image
            ])
        
        self._meralco_df = pd.DataFrame(scraped_tweets, columns=[
            'Timestamp',
            'Tweet ID',
            'Username',
            'Text',
            'Image URL'
        ])
    
    def ocr_meralco_outages(self):
        for _, row in self._meralco_df.iterrows():
            # Check if the tweet has an attached image
            if row['Image URL'] is not None:
                # Download the image
                response = get(row['Image URL'], stream=True)

                # Create a PIL image from the response
                image = Image.open(response.raw)

                # Get image dimensions
                width, _ = image.size

                # Crop image and perform OCR
                outage_date = ocr_cropped(image, (85, 220, 480, 350))
                outage_time = ocr_cropped(image, (85, 385, 480, 480))
                outage_area = ocr_cropped(image, (490, 110, width, 325))
                outage_areas = ocr_cropped(image, (520, 390, width, 910))
                new = pd.DataFrame({'Tweet ID':[row["Tweet ID"]],
                                    'Username':[row["Username"]],
                                    'Outage Area':[outage_area],
                                    'Outage Date':[outage_date],
                                    'Outage Time':[outage_time],
                                    'Affected Areas':[outage_areas]})

                # Append OCR'd info to dataframe
                self._meralco_info = pd.concat([self._meralco_info, new])

                # Delete the response
                del response
