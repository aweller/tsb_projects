#TODO

# - dict that translates nocall reason code into full explanation

# - logging
# - how to give false-pos/neg likelihood? is there a value that might be translated to e.g. small/medium/high likelihood?
# - function for natural language reporting

import variant_class as vc
import parser_functions as parser
import sys
import os
    

def find_sample_pairs_to_run(foldername, compared_trait, output_dir):
    """ Run all pairs in a folder if they only differ in a given trait """
    
    pairs = []
    
    other_traits = ["sample", "chp", "ir"]
    other_traits.remove(compared_trait)
    
    sample_dir = "all_nhs_datasets/"
    all_files = [x for x in os.listdir(sample_dir) if x.endswith("vcf")]

    for target_file in all_files:
        for comp_file in all_files:
            
            if all([parser.runs[target_file][trait] == parser.runs[comp_file][trait] for trait in other_traits]):
                if not parser.runs[target_file][compared_trait] == parser.runs[comp_file][compared_trait]:
                    pair = [target_file, comp_file]
                    
                    pair.sort(key=lambda filename: parser.runs[filename][compared_trait])
     
                    if pair not in pairs:
                           pairs.append(pair)

    ############################################################# 
    
    
    for pair in pairs:
        print pair        
        run_vcf_comparison(foldername, pair[0], pair[1], output_dir)    


def run_all_similar_files_in_folder(foldername):                
    
    """" Run all files in a folder if they have the same sample name """
    
    all_files = [x for x in os.listdir(foldername) if x.endswith(".vcf")]
    
    pairs = []
    
    for first in all_files:
        run = first.split("_")[0]
        
        pair = [x for x in all_files if run in x]
        
        if len(pair) == 1:
            pair = [pair[0], pair[0]]
        
        pair.sort()
        
        if pair not in pairs:
            pairs.append(pair)
    
    #############################################################
    
    for pair in pairs:
        print "#############################################"
        run_vcf_comparison(foldername, pair[0], pair[1])  

def run_whole_folder_in_fake_pairs(foldername):                
    
    """" Run all files in a folder against themselves (to call the variants even if theres no actual comparison) """
    
    all_files = [x for x in os.listdir(foldername) if x.endswith(".vcf")]
    
    pairs = []
    
    for first in all_files:
        for second in all_files:
            if first == second:
                pair = [first, second]
                pair.sort() 
                
                if pair not in pairs:
                    pairs.append(pair)
    
    #############################################################
    
    for pair in pairs:
        print "#############################################"
        run_vcf_comparison(foldername, pair[0], pair[1], output_dir)  
        
    
def run_vcf_comparison(foldername, oldfile, newfile, output_dir):
    
    variants = {}
    
    comp_name = "".join([oldfile.split(".")[0], "_vs_", newfile.split(".")[0]])
    
    ####################################
    # collect data

            
    with open(foldername+oldfile) as old:
        
        annotation_file = oldfile.split(".")[0] + ".tsv"
        datasets = parser.parse_datafiles(foldername+annotation_file) 
        
        for row in old:
            if row[0] == "#" or "IMPRECISE" in row: continue
            var = vc.VCFrow(row, datasets, oldfile.split(".")[0])
            
            #cutoffs = [["DP", ">", 10], ["DP", "<", 15]]
            #print var.passes_qc(cutoffs), row,
            
            variants[var.chrompos] = vc.VariantComparison()
            variants[var.chrompos].add_old(var)
    
    with open(foldername+newfile) as new:
        
        annotation_file = newfile.split(".")[0] + ".tsv"
        datasets = parser.parse_datafiles(foldername+annotation_file) 
        
        for row in new:
            if row[0] == "#" or "IMPRECISE" in row: continue
            var = vc.VCFrow(row, datasets, newfile.split(".")[0])
            var.chrompos
    
            if not variants.get(var.chrompos):
                variants[var.chrompos] = vc.VariantComparison()
                variants[var.chrompos].add_new(var)
                
            else:
                variants[var.chrompos].add_new(var)
    
    print "parsed variants for %i locations" % (len(variants))
    ####################################
    # print 
    
    dataset = vc.ComparisonDataset(variants.values())
    dataset.print_to_file(comp_name, "comparison", "all_positions", output_dir)
    dataset.print_to_file(comp_name, "comparison", "actionable_variants", output_dir)
    dataset.print_to_file(comp_name, "comparison", "all_variants", output_dir)
#     dataset.print_to_file(comp_name, "comparison", "indels")

def main():
#     target_trait = sys.argv[1]
#     find_sample_pairs_to_run("all_datasets/", target_trait)

    foldername = sys.argv[1]
    compared_trait = sys.argv[2]
    output_dir = sys.argv[3]

#     run_whole_folder_in_fake_pairs(foldername)
    find_sample_pairs_to_run(foldername, compared_trait, output_dir)

##########################################################################################################################
##########################################################################################################################


if __name__ == '__main__':
    main()

