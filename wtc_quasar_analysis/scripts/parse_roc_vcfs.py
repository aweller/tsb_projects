from pprint import pprint
import sys
import os

sys.path.append("/home/ionadmin/andreas/core/general/scripts")
import variant_class as vc
import parser_functions as parser

target_folder = "/home/ionadmin/andreas/projects/wtc_quasar_analysis/data/quasar_bams/"
target_files = [x for x in os.listdir(target_folder) if x.endswith("vcf") and "small_variants_Q" in x]

######################################################################################################

for filename in target_files:
    
    f = filename.split(".")[0].split("_")
    sample = "_".join(f[2:5])
    
    if "strand_bias" in filename:
        parameter_type = "strand_bias"
        parameter_level = f[7]
    else:
        parameter_type = f[5]
        parameter_level = f[6]  
    
    
    with open(target_folder + filename) as vcf:
        
        for row in vcf:
            if row[0] == "#" or "IMPRECISE" in row: continue
                        
            var = vc.VCFrow(row, filename=filename.split(".")[0])
            
            var_len = abs(len(var.ref) - len(var.alt))
            var_type = var.TYPE.split(",")[0]
            
            output = [sample, parameter_type, parameter_level, var.chrom, str(var.pos), var.ref+var.alt, var_type, str(var.qual), str(var_len)]
            
            print "\t".join(output)