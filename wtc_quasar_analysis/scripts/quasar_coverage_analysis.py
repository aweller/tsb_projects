import pandas as pd
import numpy as np
import seaborn as sns

header_names = ["sample", "amplicon", "gene", "gc","depth","fwd_reads","rev_reads"]
df = pd.read_csv("C:\Users\wellera\\bioinfo\wt_validation\quasar\quasar_coverage_analysis\quasar_coverage.txt", sep = "\t", header = None, names = header_names)

##############################################################################################################
# plot the mean depth across each group

sns.distplot(df.depth.groupby(df.sample).mean(), rug=False, hist=True, axlabel = "Mean coverage per sample")
sns.distplot(df.depth.groupby(df.amplicon).mean(), rug=False, hist=True, axlabel = "Mean coverage per amplicon")
sns.distplot(df.depth.groupby(df.gene).mean(), rug=False, hist=True, bins = 10, axlabel = "Mean coverage per gene")

##############################################################################################################
# Find bad samples: investigate failed amplicons per sample  

bad = df[df.depth < 10] # define bad amplicons as having > 10 depth 

amplicon_no = df.amplicon.groupby(df.sample).count() # get the total no of unique amplicons, 3126

badsamples = bad.sample.groupby(df.sample).count()
badsamples_percent = 100 * (badsamples/ amplicon_no) # define a series as % of bad amplicons

sns.distplot(badsamples_percent, rug=False, hist=True, axlabel = "Percentage of missed amplicons per sample")

# get the worst samples
# badsamples_percent[badsamples_percent > 3]
# 
# Q2PL2_6C           3.294946
# Q2PL2_7B           4.126679
# QUASAR2pl1_D03     4.926424
# QUASAR2_E02        9.436980
# Q2PL2_6H          10.460653

samples = df.depth.groupby(df.sample).mean() # mean depth per sample

sample_df = pd.DataFrame([samples, badsamples_percent]) # define new DF of mean cov and % missed amplicons 
sns.lmplot("badsamples_percent", "mean_depth", sample_df)

sample_df.sort("badsamples_percent")[-10:]
# The 2 outliers are
#
# QUASAR2_E02 (good overall coverage, many missed amplicons)
# 9.436980 977.070431
# Q2PL2_6H (bad overall coverage, many missed amplicons)
# 10.460653 27.903249

##############################################################################################################
# Find bad amplicons: investigate failed amplicons 

(df.amplicon[df.depth < 10].count() / 384498.0) * 100 # % of amplicons under 10X
# 1.4371986330227986
(df.amplicon[df.depth < 1].count() / 384498.0) * 100 # % of uncovered amplicons 
# 0.2270492954449698

# create series
amplicon_missed = bad.amplicon.groupby(df.amplicon).count()
amplicon_meandepth = df.depth.groupby(df.amplicon).mean()

# merge series into new DF for plotting
df1 = pd.DataFrame(amplicon_missed)
df2 = pd.DataFrame(amplicon_meandepth)
df3 = pd.merge(df1, df2, left_index=True, right_index=True, how="outer")
df3["mean_depth"] = df3["0_y"]
df3["miss_amplicons"] = df3["0_x"]
df3 = df3.fillna(0)
sns.lmplot("mean_depth", "miss_amplicons", df3)

# get genes with most missing amplicons

amplicon_missed = bad.amplicon.groupby([df.amplicon,df.gene]).count()
amplicon_missed = amplicon_missed.reset_index()
df6 = amplicon_missed.missed.groupby(amplicon_missed.gene).sum()
df6.sort()
df6[-10:]

# gene
# BRCA2     178
# AR        181
# TNKS2     185
# WT1       186
# JAK2      204
# PIK3CA    222
# JAK3      276
# MAP3K1    310
# ATM       338
# NOTCH1    376



