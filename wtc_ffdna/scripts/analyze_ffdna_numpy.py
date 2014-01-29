# workflow used for ffDNA spikeins: AmpliSeq CHP2_v2 single samples oncomine 1_6_2                                            

# activate the virtualenv for scipy and pandas
activate_this_file = "/home/ionadmin/andreas/core/andreas_python/bin/activate_this.py"
execfile(activate_this_file, dict(__file__=activate_this_file))

import sys
sys.path.append("/home/ionadmin/andreas/core/general/scripts")
import variant_class as vc

import os
import scipy
import numpy as np
import pandas as pd

cosmics = ["522","6255","516","6240","473","520","6224","476","532","6218**/133189","763"]
genes = ["KRAS","EGFR","KRAS","EGFR","BRAF","KRAS","EGFR","BRAF","KRAS","EGFR","PIK3CA"]
mutations = ["G12A","L747_S752","G12C","T790M","V600K","G12V","L858R","V600E","G13D","L747_E749","E545K"]
chroms = [12, 7, 12, 7, 7, 12, 7,7,12,7,3]
kits = ["A", "A","B","B","B","C","C","C","D","D","D"]
positions = [25398284,55242468,25398285,55249071,140453137,25398284,55259515,140453136,25398281,55242465,178936091]
nt_change = ["c.35G>C","ATTAAGAGAAGCAACATCT/ATTAAGAGAAGCAACATCT","c.34G>T","c.2369C>T","c.1798_1799GT>AA","c.35G>T","c.2573T>G","c.1799T>A","c.38G>A","GGAATTAAGAGAAGCAACATCT/GGAATTAAGAGAAGCAACATCT","c.1633G>A"]
ff_strand_nt_change = ["C>G","ATTAAGAGAAGCAACATCT>A","C>A","C>T","C>T","C>A","T>G","A>T","C>T","GGAATTAAGA>G","G>A"]

target_variants = {"A" : [25398284, 55242468],
"B" : [25398285, 55249071, 140453137],
"C" : [25398284, 55259515, 140453136],
"D" : [25398281, 55242465, 178936091]}

control_reads = {25398284:[], 55242468:[], 25398285:[], 55249071:[], 140453137:[], 
                25398284:[], 55259515:[], 140453136:[], 25398281:[], 55242465:[], 178936091:[]}

spiked_reads = {25398284:None, 55242468:None, 25398285:None, 55249071:None, 140453137:None, 
                25398284:None, 55259515:None, 140453136:None, 25398281:None, 55242465:None, 178936091:None}

ffnda_folder = "../data/ffdna/"

all_reads = {}
keys_in_order = []

for i in range(len(positions)):
    kit = "kit" + kits[i]
    pos = positions[i]
    ref = ff_strand_nt_change[i].split(">")[0]
    alt = ff_strand_nt_change[i].split(">")[1]
    
    key = "_".join([kit,str(pos),alt])
    
    keys_in_order.append(key)
    
    all_reads[key] = {} 
    all_reads[key] = {}


###########################################################################################################
# collect relevant variants 

def extract_kit_from_filename(target_file):
    basename = target_file.split("_")[3]
    kit = basename[-2]
    kit_no = basename[-1]
    return kit+kit_no
    
ffdna_files = [x for x in os.listdir(ffnda_folder) if x.endswith(".vcf") and x.startswith("hotspot_calls_50g")
                and "dataqual" not in x and "_R-" in x and "AV" not in x]

ffdna_files.sort()
print ffdna_files

df = pd.DataFrame(columns = [keys_in_order], 
                  index = [extract_kit_from_filename(x) for x in ffdna_files])


for target_file in ffdna_files:
    basename = target_file.split("_")[3]
    
    kit = basename[-2]
    kit_no = basename[-1]
    file_row = [kit+kit_no,]
    
#     print "reading", basename, kit, kit_no
    
    with open(ffnda_folder + target_file) as vcf:
        for row in vcf:
            if row[0] == "#": continue
            var = vc.VCFrow(row, None, target_file.split(".")[0])
                       
            if var.pos in positions: # its a relevant variants
                #print target_file, row,
                
#                 if var.pos == 140453136: print row,
                
                for key in all_reads.keys():
                    target_kit = key.split("_")[0]
                    target_pos = int(key.split("_")[1])
                    target_alt = key.split("_")[2]
                                        
                    if var.pos == target_pos:
                        
                        if len(var.alt.split(",")) == 1: # a single allele was tested, needs to be saved once
                            if var.alt == target_alt: # this is the correct variant
                                df[key][kit+kit_no] = int(var.AO)
                                
                                if "kit" + kit == target_kit: # save as spiked
                                    all_reads[key][target_file] = [int(var.AO), int(var.DP)]
                                else: # save as control
                                    all_reads[key][target_file] =[int(var.AO), int(var.DP)]
                                    
                                
                                
                        elif len(var.alt.split(",")) > 1: # two alleles were tested, needs to be saved to 2 keys
                            first_allele = var.alt.split(",")[0]
                            first_AO = [int(var.AO.split(",")[0]), int(var.DP)]
                                                                       
                            second_allele = var.alt.split(",")[1]
                            second_AO = [int(var.AO.split(",")[1]), int(var.DP)]
                            
                            if first_allele == target_alt:
                                correct_allele = first_allele
                                correct_AO = first_AO
                            
                            elif second_allele == target_alt:
                                correct_allele = second_allele
                                correct_AO = second_AO
                            #
                            #print "first, second, target", first_allele, second_allele, target_alt
                            #print "AO:", var.AO
                            #print "correct AO:", correct_AO
                            
                            df[key][kit+kit_no] = correct_AO[0]
                            
                            if "kit" + kit == target_kit: # save as spiked
                                all_reads[key][target_file] = correct_AO
                                #print "saved as spiked in ", key
                            else: # save as control
                                all_reads[key][target_file] = correct_AO
                                #print "saved as control in ", key
                            
#                         if target_file == "hotspot_calls_50g_B2_hp2_somatic_lowstringency_chp2_hotspots_noheader.vcf":
#                             print var.chrompos, var.AO, target_kit
                           
############################################################################################################
## analyze each position

df.to_csv("ffdna_results2.tsv", sep='\t')

for key in keys_in_order:
    target_kit = key.split("_")[0]
    target_pos = int(key.split("_")[1])
    target_alt = key.split("_")[2]
    
    curr_kit = target_kit[3]

    control = df.loc[[x for x in df.index if curr_kit not in x], key].mean()
    
    for x in df.loc[[x for x in df.index if curr_kit in x], key]:
        print key, x, control

# for target_file in ffdna_files:
#     basename = target_file.split("_")[3]
#     
#     kit = basename[-2]
#     kit_no = basename[-1]
#     
#     results_row = [kit+kit_no,]
#     
#     for key in keys_in_order:
#         AO = all_reads[key][target_file][0]
#         DP = all_reads[key][target_file][1]
#         
#         freq = round(AO/float(DP), 4)
#         
#         results_row.extend([AO, DP, freq])
#         
#     print "\t".join([str(x) for x in results_row])
    
    

# for key in sorted(all_reads.keys()):
#     
#     spiked = all_reads[key]["spiked"]
#     control = all_reads[key]["control"]
#     
#     spiked.sort()
#     control.sort()
#     
#     print "-----------------"
#     print key
#     print spiked
#     print control
    

#for position, vars in control_reads.iteritems():
#    if spiked_reads[position]:
#    
#        control_alt_mean = scipy.mean([int(var.FAO) for var in vars])
#        control_cov_mean = scipy.mean([int(var.FDP)+int(var.FAO) for var in vars])
#        print [int(var.FAO) for var in vars], [int(var.FDP)+int(var.FAO) for var in vars]
#        
#        spiked_alt = int(spiked_reads[position].FAO)
#        spiked_cov = int(spiked_reads[position].FDP) + int(spiked_reads[position].FAO)
#        
#        index = positions.index(position)
#        
#        print "\t".join([str(x) for x in [position, genes[index], spiked_alt, spiked_cov, control_alt_mean, control_cov_mean]])