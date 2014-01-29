import os
import sys
sys.path.append("/home/ionadmin/andreas/core/general/scripts")
import variant_class as vc
import pprint

vcf_folder = "/home/ionadmin/andreas/projects/wtc_quasar_analysis/data/quasar_vcfs/"
quasar_vcfs = [vcf_folder + x for x in os.listdir(vcf_folder) if x.endswith("vcf") and x.startswith("Q")]
out_fields = ["ref", "alt", "DP", "FAO", "FDP", "FRO"]

for quasar_vcf in quasar_vcfs:
    with open(quasar_vcf) as vcf:
        vcf_name = quasar_vcf.split("/")[-1]
        all_snps = {}
        total_snps = 0
        
        for row in vcf:
            
            if row.startswith("#"): continue
    
            var = vc.VCFrow(row, filename=quasar_vcf)
            
            f= row.strip().split("\t")
            ref, alt = f[3], f[4]
            
            if not len(ref)+len(alt) == 2: continue
            
            snp = ref+alt
            
            if not all_snps.get(snp):
                all_snps[snp] = 0
                
            all_snps[snp] += 1
            total_snps += 1
            
            print "\t".join([vcf_name, ref+alt])
            
    try:       
        CT_to_GA = round( all_snps["CT"]/float(all_snps["GA"]), 1 )
        CT_GA_no = all_snps["CT"]+all_snps["GA"]
        CT_percent_of_total = round( CT_GA_no / float(total_snps), 2 )

    
    except:
        CT_to_GA, CT_percent_of_total, CT_GA_no = "NA","NA","NA"
        
         
#     print CT_percent_of_total, CT_GA_no, total_snps, vcf_name
    
