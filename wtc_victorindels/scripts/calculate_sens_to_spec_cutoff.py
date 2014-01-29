import os
import sys
sys.path.append("/home/ionadmin/CallValidation/")
import variant_class as vc
import matplotlib.pyplot as plt

def parse_vcf(filename, hotspots, qc_cutoff):
    
    vcf_rows = []
    
    # provide fake datasets which the class expects 
    datasets = {}
    datasets["annotations"] = {}
    
    with open(filename) as vcf:        
        for row in vcf:
            
            in_hotspot = False
            passes_cutoff = False
            
            if row[0] == "#" or "PASS" not in row: continue

            var = vc.VCFrow(row, datasets, filename)
            
            if hotspots.get(var.chrom):
                for interval in hotspots[var.chrom]:
                    if interval[0] < var.pos < interval[1]: 
                        in_hotspot = True
                        break
            
            if in_hotspot and var.passes_custom_cutoff(qc_cutoff) and var.TYPE != "snp":
                vcf_rows.append(var)
    
    return vcf_rows

def get_sens_and_spec(dataset):
    
    samples_tested = len(dataset)
    
    empty = len([x for x in dataset if not x])
    nonempty = samples_tested - empty
    sens = nonempty/float(samples_tested) 
    
    true_pos = 0
    false_pos = 0
    for vars in dataset:
        if len(vars) >0:
           true_pos += 1
        if len(vars) >1:
           false_pos += (len(vars)-1) 
    
    spec = true_pos/float(true_pos+false_pos)
    
    return sens, spec

def run_all_for_qc_cutoff(qc_cutoff):
    
    hotspots = {"chr17":[[7578334, 7578578], [7578137, 7578321], [7577471, 7577631], [7576997, 7577187]],"chr4":[[153249334, 153249581], [153247124, 153247406]] }
    rerun_folder = "/home/ionadmin/CallValidation/RerunTVC/"
    missing_codes = ["9A", "9C", "9G", "574"]
        
    tvc_settings = ["hp2_somatic_lowstringency", "lowpredshift_vic",
        "lowpredshift_nostrandbia_vic", "nopredshift_nostrandbia_vic", "nostrandbias_longindel_vic"]
    
    folders = [x for x in os.listdir(rerun_folder) if x.startswith("VICindels_")]
    codes = [x[10:] for x in folders if x[10:] not in missing_codes]
    
    all_rows = {}
    
    for code in codes:
    
        code_folders = [x for x in folders if code in x]
    
        for folder in code_folders:
            all_vcfs = [file for file in os.listdir(rerun_folder + folder) if file.endswith("_vicindel_whole_genes.vcf") 
                        and file.startswith("small_variants_VIC")]
            
            for vcf in all_vcfs:
                short_filename = vcf.split("/")[-1].lstrip("small_variants_VICindels_").rstrip("_whole_genes.vcf")
                all_rows[short_filename] = parse_vcf(rerun_folder + folder + "/" + vcf, hotspots, qc_cutoff)     
                    
    ################################################################################################
    # walk through settings
    
    for setting in tvc_settings:
                
        dataset = [all_rows[short_filename] for short_filename in all_rows.keys() if setting in short_filename]
        print [len(item) for item in dataset]     
        sens, spec =  get_sens_and_spec(dataset)
        
        print i, setting, sens, spec

################################################################################################

for i in [0, 2.5, 5]:
    
    fao = "self.FAO > %i" % (i*10)
    fro = "self.FRO > %i" % (i*100)

    qc_cutoff = [fao, fro]
    run_all_for_qc_cutoff(qc_cutoff)
