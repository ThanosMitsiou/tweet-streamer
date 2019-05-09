from tweepy import StreamListener, Stream
from utils import get_access


class TweetListener(StreamListener):

    def __init__(self, track, is_async):
        self.api = get_access()
        self.stream = Stream(auth=self.api.auth, listener=self)
        self.stream.filter(track=track, is_async=is_async, languages=["en"])

    def on_status(self, status):
        # populate kafka
        print(self.get_full_text(status))

    def on_error(self, error_code):
        if error_code == 420:
            return False

    @staticmethod
    def get_full_text(status):
        if hasattr(status, "retweeted_status"):
            try:
                text = status.retweeted_status.extended_tweet["full_text"]
            except:
                text = status.retweeted_status.text
        else:
            try:
                text = status.extended_tweet["full_text"]
            except AttributeError:
                text = status.text

        return text


tweet_listener = TweetListener(track=["#btc"], is_async=True)

