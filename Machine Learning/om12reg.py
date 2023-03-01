import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.utils import shuffle

data = pd.read_csv('FirstCleanData.csv')

df = pd.DataFrame(data)
ax1 = df.plot(kind='scatter',x='OM1',y='LASK1',color='r')
#ax2 = df.plot(kind='scatter',x='2',y='1.1',color='g',ax=ax1)
#ax3 = df.plot(kind='scatter',x='3',y='1.1',color='b',ax=ax1)
#ax4 = df.plot(kind='scatter',x='4',y='1.1',color='orange',ax=ax1)
#ax5 = df.plot(kind='scatter',x='5',y='1.1',color='purple',ax=ax1)
#ax6 = df.plot(kind='scatter',x='6',y='1.1',color='yellow',ax=ax1)
#ax7 = df.plot(kind='scatter',x='7',y='1.1',color='cyan',ax=ax1)
#ax8 = df.plot(kind='scatter',x='8',y='1.1',color='magenta',ax=ax1)
#ax9 = df.plot(kind='scatter',x='9',y='1.1',color='black',ax=ax1)
#ax10 = df.plot(kind='scatter',x='10',y='1.1',color='g',ax=ax1)
#ax11 = df.plot(kind='scatter',x='11',y='1.1',color='black',ax=ax1)
#ax12 = df.plot(kind='scatter',x='12',y='1.1',color='orange',ax=ax1)
#data.head()
plt.xlabel('band 1')
plt.ylabel('lask 1')
plt.show()

