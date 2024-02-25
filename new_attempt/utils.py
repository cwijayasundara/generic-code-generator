import os
import pandas as pd


def safe_write(path, code):
    path = "./software/" + path
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+') as f:
        f.write(code)


df = pd.read_csv("rules/expanded_trade_attributes.csv")


def attributes():
    df_attributes = df["Attributes"].tolist()
    """ return a comma separated string of the attributes in the df. """
    return ', '.join(df_attributes)


def attribute_validations():
    df_attributes = df["Attributes"].tolist()
    df_attribute_validations = df["Attribute Validations"].tolist()
    """ loop over the df_attributes and df_attribute_validations and create a dictionary 
    with the attributes as the key and the attribute_validations as the value."""
    attribute_validations_dict = {}
    for i in range(len(df_attributes)):
        attribute_validations_dict[df_attributes[i]] = df_attribute_validations[i]
    return attribute_validations_dict


def business_rules():
    df_attributes = df["Attributes"].tolist()
    df_business_rules = df["Business Rules"].tolist()
    """ loop over the df_attributes and df_business_rules and create a dictionary
    with the attributes as the key and the business_rules as the value."""
    business_rules_dict = {}
    for i in range(len(df_attributes)):
        business_rules_dict[df_attributes[i]] = df_business_rules[i]
    return business_rules_dict
