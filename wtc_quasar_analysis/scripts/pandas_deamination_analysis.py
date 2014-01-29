import pandas as pd
import numpy as np
import seaborn as sns

header_names = ["sample", "snp"]
df = pd.read_csv("C:\Users\wellera\\bioinfo\wt_validation\quasar\deamination\quasar_snps.txt", sep = "\t", header = None, names = header_names)

snps_per_sample = df.snp.groupby(df.sample).count()

#############################################################################
# get C -> T

ct_per_sample = df[df.snp.isin(["CT", "GA"])].snp.groupby(df.sample).count()

df1 = pd.DataFrame(ct_per_sample)
df2 = pd.DataFrame(snps_per_sample)

sample_df = pd.merge(df1, df2, left_index=True, right_index=True, how="outer")

sample_df["ct"] = sample_df["0_x"]
sample_df["snps"] = sample_df["0_y"]
sample_df["ct_ratio"] = sample_df["ct"] / sample_df.snps

sns.lmplot("snps", "ct_ratio", sample_df)
plt.title("Total variants vs ratio of C->T mutations")