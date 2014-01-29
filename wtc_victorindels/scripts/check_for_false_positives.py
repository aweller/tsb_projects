import os
import sys
sys.path.append("/home/ionadmin/CallValidation/")
import variant_class as vc

################################################################################################

def check_vcf(filename):
    
    # provide fake datasets which the class expects 
    datasets = {}
    datasets["annotations"] = {}
    
    hotspots = []
    
    with open(filename) as vcf:
        stats = {"vars":0, "hotspot":0, "indels":0, "qc":0}
        
        for row in vcf:
            
            in_hotspot = False
            passes_cutoff = False
            
            if row[0] == "#" or "PASS" not in row: continue

            var = vc.VCFrow(row, datasets, folder)
            stats["vars"] += 1
            
            if var.chrom == "chr17":
                for interval in tp_53:
                    if interval[0] < var.pos < interval[1]: 
                        in_hotspot = True
            elif var.chrom == "chr4":
                for interval in fbxw7:
                    if interval[0] < var.pos < interval[1]: 
                        in_hotspot = True 
        
            
            if in_hotspot:
                stats["hotspot"] += 1

                if var.TYPE != "snp":
                    stats["indels"] += 1
                                    
                    if all([var.FAO>50, var.FRO>500]):
                        stats["qc"] += 1
                        passes_cutoff = True
    
    ############################################################################################
    
    short_filename = filename.split("/")[-1].lstrip("small_variants_VICindels_").rstrip("vcf")
    
    # to get an overview of all files    
#     out =  "-".join([str(x) for x in [stats["hotspot"], stats["qc"]]]) 

    # to get stats across files
    out =  [stats["hotspot"], stats["qc"]] 

    return short_filename, out 


################################################################################################


rerun_folder = "/home/ionadmin/CallValidation/RerunTVC/"
tp_53 = [[7578334, 7578578], [7578137, 7578321], [7577471, 7577631], [7576997, 7577187]]
fbxw7 = [[153249334, 153249581], [153247124, 153247406]]

folders = [x for x in os.listdir(rerun_folder) if x.startswith("VICindels_")]
codes = [x[10:] for x in folders]
missing_codes = ["9A", "9C"]

results = {"no_qc":{1:[],2:[],3:[]},
           "nhs_qc":{1:[],2:[],3:[]}}

for code in codes:
    if code in missing_codes: continue
    
    outrow = [code, "X", "X", "X"]
    
    code_folders = [x for x in folders if code in x]
    for folder in code_folders:
        all_vcfs = [file for file in os.listdir(rerun_folder + folder) if file.endswith(".vcf") and "small_variants_VIC" in file
                    and ("hp2" in file or "pred" in file) and "whole" in file]
        
        for vcf in all_vcfs:
            short_filename, out = check_vcf(rerun_folder + folder + "/" + vcf)
            cutoff_level = None
            
            if "hp2" in short_filename:
                outrow[1] = "-".join([str(x) for x in out])
                cutoff_level = 1                
            elif "lowpredshift_nostrandbia" in short_filename:
                outrow[2] = "-".join([str(x) for x in out])
                cutoff_level = 2
            elif "nopredshift_nostrandbia" in short_filename:
                outrow[3] = "-".join([str(x) for x in out])
                cutoff_level = 3
            
            if cutoff_level: 
                results["no_qc"][cutoff_level].append(out[0])
                results["nhs_qc"][cutoff_level].append(out[1])

                
    print "\t".join(outrow)
                
##################################################################

for qc in ["no_qc", "nhs_qc"]:
    for cutoff in [1,2,3]:
        data = results[qc][cutoff]
        
        samples = len(data)
        missed = data.count(0)
        pos_samples = samples - missed
        total_found = sum(data)
        
        sens = pos_samples/float(samples) 
        spec = 
        
        print qc, cutoff, sum(results[qc][cutoff]), results[qc][cutoff]


            
