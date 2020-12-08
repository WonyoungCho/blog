#! /usr/bin/env python3

import pandas as pd
import numpy as np


def FormatData(path, sep = '\t', chromosome, p_value):
    data = pd.read_table(path, sep = sep)
    data['-log10(p_value)'] = -np.log10(data[p_value])
    data[chromosome] = data[chromosome].astype('category')
    data['ind'] = range(len(data))
    data_grouped = data.groupby((chromosome))
    return data, data_grouped

