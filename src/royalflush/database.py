##encoding=utf-8

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.royalflush
score = db.score
seven_cards_score = db.seven_cards_score
odds = db.odds
threaten = db.threaten


if __name__ == "__main__":
    print(db.command("dbstats"))
    print(seven_cards_score.find().count())
    pass