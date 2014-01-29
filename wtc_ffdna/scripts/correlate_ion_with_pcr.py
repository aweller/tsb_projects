import pandas as pd

head  = ["loc", "conc", "ion", "pcr"]
bad = ["N/D",]

df = pd.read_csv("castPCR_results.txt", delimiter="\t", header = None)
df.columns = head

df[['ion', 'pcr']] = df[['ion', 'pcr']].astype(float)

newdf = df[~df['pcr'].isin(bad)]
df = newdf[~newdf['ion'].isin(bad)]

small = df["conc"].isin(["0.01%", "0.05%"])
big = ~df["conc"].isin(["0.01%", "0.05%"])  
smalldf = df[small]
bigdf = df[big]

plt.scatter(bigdf["ion"], bigdf["pcr"])
plt.scatter(smalldf["ion"], smalldf["pcr"])

from scipy import stats
import scipy

scipy.stats.pearsonr(bigdf["ion"], bigdf["pcr"])
scipy.stats.pearsonr(smalldf["ion"], smalldf["pcr"])

# scipy.stats.pearsonr(bigdf["ion"], bigdf["pcr"])
# Out[50]: (0.54871274890550692, 0.0016907580171039228)
# 
# scipy.stats.pearsonr(smalldf["ion"], smalldf["pcr"])
# Out[51]: (-0.022719057217630366, 0.92006319963935879)

import seaborn as sns

df["Class"] = df['conc'].isin(["0.05%","0.01%"])
df["<0.01%"] = df["Class"]

sns.lmplot("ion", "pcr", df, color = "< 0.1%")
plt.title("Correlation of spiked-in mutations")
plt.ylabel("castPCR % Mutation")
plt.xlabel("Ion PGM reads")
plt.ylim(-2, 8)