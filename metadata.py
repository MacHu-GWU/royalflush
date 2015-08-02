##encoding=utf-8

import pickle

def load_pk(abspath):
    """load object from pickle file"""
    print("loading %s ..." % abspath)
    with open(abspath, "rb") as f:
        obj = pickle.load(f)
    return obj

seven_cards_score_dict = dict()
for filename in [r"project\seven_cards_score_%s.pickle" % i for i in range(1, 14+1)]:
    for k, v in load_pk(filename).items():
        seven_cards_score_dict[k] = v