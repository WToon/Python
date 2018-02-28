import pandas as pd
from matplotlib import style
import numpy as np
import matplotlib.pyplot as plp

style.use('ggplot')

web_stats = {'Day': [1, 2, 3, 4, 5, 6],
             'Visitors': [43, 53, 34, 45, 64, 34],
             'Bounce_Rate': [65, 72, 62, 64, 54, 66]}

df = pd.DataFrame(web_stats)

df.set_index('Day', inplace=True)
print(df)
# print(df.Visitors)
# print(df[['Visitors', 'Bounce_Rate']])
print(df.Visitors.tolist())
print(np.array(df[['Visitors', 'Bounce_Rate']]))


plp.plot(df.Visitors)
plp.plot(df.Bounce_Rate)
plp.show()
