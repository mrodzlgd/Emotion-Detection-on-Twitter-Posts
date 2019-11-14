import pandas as pd
import re

def ReplaceThreeOrMore(s):
    # pattern to look for three or more repetitions of any character, including
    # newlines.
    pattern = re.compile(r"(.)\1{2,}", re.DOTALL) 
    return pattern.sub(r"\1\1", s)


def remove_hashtags(series):
    no_hash = series.apply(lambda x: re.sub('#[\w]*', "", x))
    return no_hash