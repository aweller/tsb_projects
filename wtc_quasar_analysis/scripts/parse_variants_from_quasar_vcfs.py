from pprint import pprint
import sys
import os

sys.path.append("/home/ionadmin/andreas/core/general/scripts")
import variant_class as vc
import parser_functions as parser

target_folder = "/home/ionadmin/andreas/projects/wtc_quasar_analysis/data/quasar_vcfs/"
target_files = [x for x in os.listdir(target_folder) if x.endswith("vcf") and "IR16" in x]

polys = {}

cutoffs = [["int(self.FAO)>0", "int(self.FRO)+int(self.FAO)>0"],
           ["int(self.FAO)>10", "int(self.FRO)+int(self.FAO)>100"],
           ["int(self.FAO)>20", "int(self.FRO)+int(self.FAO)>200"],
           ["int(self.FAO)>30", "int(self.FRO)+int(self.FAO)>300"],
           ["int(self.FAO)>40", "int(self.FRO)+int(self.FAO)>400"],
           ["int(self.FAO)>50", "int(self.FRO)+int(self.FAO)>500"]]
           

field_order = [ 'filename',
                'samplename',

 'chrom',
  'pos',

 'ref',
 'alt',
 'alt_consensus',
 'alt_percent',
 'gid',
 'loc',
  'func',
   'type',

 'in_blacklist',

'FR',
 'FreqT',
 'RBI',
 'GQ',
 'total_reads',
 'VARB',
 'FSAF',
 'DP',
 'SXB',
 'p-value',
 'FSRR',
 'FWDB',
 'OREF',
 'REVB',
 'SAF',

 'FSRF',
 'FAO',
 'SAR',
 'ir_version',
 'RO',
 'OPOS',
 'MLLD',
 'GT',
 'SRF',
 'STB',
 'OALT',
 'genes',
 'FRO',
 'AO',
 'HRUN',
 'FSAR',
 'qual',
 'REFB',
 'OMAPALT',
 'SRR',
 'SSEP',
 'FDP',
 'OID',
 'LEN',
 'FreqN',
 'omim',
 'is_variant',
 'SSEN',
 'TYPE',
]

###########################################################################################################

for target_cutoff in cutoffs: 
    
    vars = 0
    exon_vars = 0
    actionable = 0
    
    print "\t".join(field_order)
    
    for filename in target_files:
        with open(target_folder + filename) as vcf:
            
            annotation_file = filename.split(".")[0] + ".tsv"
            datasets = parser.parse_datafiles(target_folder+annotation_file) 
            
            for row in vcf:
                if row[0] == "#" or "IMPRECISE" in row: continue
                            
                var = vc.VCFrow(row, datasets, filename.split(".")[0])            
#                 print var.chrompos +"\t"+ var.gid.split(":")[0]
                fields = var.__dict__         

                
                print "\t".join([str(x) for x in [fields.get(y) for y in field_order]])

#                 pprint(fields.keys())
                
#                 status = "Ref"
#                 
#                 if var.passes_custom_cutoff(target_cutoff):
#                 
#                     if var.passes_custom_cutoff(["self.is_variant == True", "self.FR == '.'"]):
#                         vars += 1
#                         if var.passes_custom_cutoff(["'exon' in self.loc"]):
#                             exon_vars += 1
#                             if var.passes_custom_cutoff(["'syn' not in self.func", "'ref' not in self.func"]):
#                                 actionable += 1
#             
#     print "\t".join([str(x) for x in [target_cutoff, vars, exon_vars, actionable]])
        sys.exit()