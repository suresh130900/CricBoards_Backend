import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def all_matches():
    matches = pd.read_csv("ipl_matches_2008_2022.csv")
    print(matches)
    return matches


