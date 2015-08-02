#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.royalflush
five_cards_score = db.five_cards_score
seven_cards_score = db.seven_cards_score

if __name__ == "__main__":
    from pprint import pprint as ppt
    ppt(db.command("dbstats"))
    print(five_cards_score.find().count()) # C(52, 5) = 2,598,960
    print(seven_cards_score.find().count()) # C(52, 7) = 133,784,560