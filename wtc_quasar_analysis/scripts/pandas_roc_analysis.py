import pandas as pd
import numpy as np
import seaborn as sns
header_names = ["sample", "parameter", "level", "chr", "pos", "refalt", "type", "qual", "len"]

df = pd.read_csv("C:\Users\wellera\\bioinfo\wt_validation\quasar\\roc\\roc_curve_dataset.txt", sep = "\t", header = None, names = header_names)

#split into separate dfs for snps and indels

snps_df = df[(df.type == "snp")]
indel_df = df[~(df.type == "snp")]

########################################################################################################
# whats the mean no. of Indels per level?

indels_per_sample = indel_df.sample.groupby([indel_df.sample, indel_df.parameter, indel_df.level]).count()
ips_df = pd.DataFrame(indels_per_sample)
ips_df = ips_df.reset_index() # move index into columns
ips_df[0].groupby(ips_df.level).mean()

# level
# 0        1.200000
# 1        1.146341
# 2        1.159091
# 3        1.318182
# 4        1.333333
# 5        1.415094
# 6        1.436364
# 7        1.473684
# 8        1.523810
# 9        1.763158
# dtype: float64