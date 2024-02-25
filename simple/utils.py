import os
import pandas as pd


def safe_write(path, code):
    path = "./software/" + path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+') as f:
        f.write(code)


df = pd.read_csv("rules/cdr_v2.csv")


def attributes():
    return df["Attributes"].tolist()


def attribute_validations():
    return df["Attribute Validations"].tolist()


def business_rules():
    return df["Business Rules"].tolist()
