# fetch IR location of bam files for the download script

import sys

sample_file = "QUASAR_samples_run_Dec2013.txt"
samples = [x.split("\t")[0] for x in open(sample_file).readlines()]

sample_count = {}
for sample in samples:
    sample_count[sample] = 0

sample_names = {}    
with open("quasar_overview.txt") as overview:
    for row in overview:
        f = row.split("\t")
        lab_sample, tumor_sample, normal_sample = f[1], f[5], f[7]
        sample_names[lab_sample] = [tumor_sample, normal_sample]


with open("IR_source_files/IonReporter_Sample_Data_3_1_2014_v2.csv") as locations:
    for row in locations:
        
        if not "bam" in row: continue
        
        for sample in samples:
            tumor_sample, normal_sample = sample_names[sample]
#             print sample, tumor_sample, normal_sample
            
            if row.startswith(tumor_sample):
                sample_count[sample] += 1
                print "\t".join([tumor_sample, row.split(",")[2]]) 
            
            elif row.startswith(normal_sample):
                sample_count[sample] += 1
                print "\t".join([normal_sample, row.split(",")[2]]) 
            
# for key, value in sample_count.items():
#     print key, value