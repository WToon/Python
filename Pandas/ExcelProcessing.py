import pandas as pd
import matplotlib.pyplot as plp
from matplotlib import style
import numpy as np
import math
style.use('ggplot')

data = pd.read_excel('DistrData.xlsx')
data['index'] = range(1, len(data) + 1)
data.set_index('index', inplace=True)

data_50 = data['Rand_0_50'].tolist()
data_100 = data['Rand_0_100'].tolist()


def to_int(x):
    for i in range(0, len(x)):
        x[i] = int(math.floor(x[i]))
    return x


data_100 = to_int(data_100)
data_50 = to_int(data_50)


def get_count(x):
    range_ = max(x)
    result = {'index': [], 'counted': []}
    for i in range(0, range_+1):
        count = 0
        for x_ in x:
            if i == x_:
                count += 1
        result.get('index').append(i)
        result.get('counted').append(count)
    return result

def get_excel_graph():
    df_50 = pd.DataFrame(get_count(data_50))
    df_100 = pd.DataFrame(get_count(data_100))
    df_50.set_index('index', inplace=False)
    df_100.set_index('index', inplace=False)
    plp.bar(df_50['index'], df_50['counted'])
    plp.bar(df_100['index'], df_100['counted'])
    print(df_50.tail())
    plp.show()
    return

def plot_sin():
    x = np.linspace(-np.pi*5, np.pi*5, 401)
    plp.plot(x, np.sin(x), color="orange")
    plp.plot(x, np.cos(x), color="red")
    plp.show()
    return

get_excel_graph()