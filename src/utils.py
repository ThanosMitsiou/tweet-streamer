import yaml
from kafka import KafkaProducer
from tweepy import OAuthHandler, API


def get_credentials(path="conf/tweet_cred.yaml"):
    credentials = yaml.safe_load(open(path))
    return credentials


def get_access():
    cred = get_credentials()

    auth = OAuthHandler(
        consumer_key=cred["consumer_key"], consumer_secret=cred["consumer_secret"]
    )

    auth.set_access_token(key=cred["access_key"], secret=cred["access_secret_key"])

    api = API(auth)
    return api


def get_producer():
    producer = KafkaProducer(bootstrap_servers=["35.188.181.255:9092"])

    print(producer)
