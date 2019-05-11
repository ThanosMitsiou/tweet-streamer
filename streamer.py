from argparse import ArgumentParser
from src.tweet_streamer import TweetListener

parser = ArgumentParser()
parser.add_argument('-t', '--track', type=str, nargs='+', dest='list',
                    help='List of items to listen to on tweets')

track_list = parser.parse_args().list

if __name__ == '__main__':
    listener = TweetListener(track=track_list, is_async=True)
