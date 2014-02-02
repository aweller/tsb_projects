# run the IR coverage plugin on a folder full of bams

import sys
import subprocess
import os

bam_folder = sys.argv[1]
bed = "~/andreas/projects/wtc_quasar_analysis/data/148_gene_panel/TSB_148_gene_panel_HP_amplicon_locations.txt"
ref_genome = "/results/uploads/hg19.fasta"
out = "/home/ionadmin/andreas/projects/wtc_quasar_analysis/data/coverage_out"
log_file = open("/home/ionadmin/andreas/projects/wtc_quasar_analysis/data/coverage_out/log.txt", "wa")

bams = [x for x in os.listdir(bam_folder) if x.endswith("bam")]
existing_files = [x for x in os.listdir(out) if x.endswith(".target.cov.xls")]

for bam in bams:

    bam_path = bam_folder + "/" + bam
        
    coverage_cmd = "/results/plugins/coverageAnalysis/scripts/run_coverage_analysis.sh -A %s -D %s %s %s"  % (bed, out, ref_genome, bam_path)
    
#     print coverage_cmd
    
    exists =False
    
    for outfile in existing_files:
        if bam.split(".")[0] in outfile:
            print "Existing", bam
            exists = True
            break
    
    if not exists:       
        print "Starting", bam
        subprocess.call(coverage_cmd, shell=True)
    



# nohup python ../../../core/run_tvc/scripts/run_tvc.py ./roc/tvc_runplan_quasar_all_combined0_and_9.txt && python ../scripts/run_coverage_plugin.py /home/ionadmin/andreas/projects/wtc_quasar_analysis/data/quasar_bams/ &