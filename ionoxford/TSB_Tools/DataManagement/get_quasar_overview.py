import pprint
import sys

def sorter(id1, id2):
    """ Sort a list of OX1-23 formatted runs """
    if int(id1[2]) > int(id2[2]):
        return 1
    elif int(id2[2]) > int(id1[2]):
        return -1
    else:
        if int(id1[4:]) > int(id2[4:]):
            return 1
        elif int(id2[4:]) > int(id1[4:]):
            return -1    
        
analysis_summary_header = ["IR_Version","Tumour_Sample","Normal_Sample","Analysis_Name","Workflow","Status","User","Date"]
spreadsheet_header = ["Lab_Sample","Run","IR_sample","IR_filetype","IR_Version","Tumour_Sample","Normal_Sample","Analysis_Name","Workflow","Status","User","Date"]
output_header = ["Lab_Sample","Run","IR_sample","Tumour_Barcode", "Tumour_Sample", "Normal_Barcode", "Normal_Sample","Analysis_Name","Workflow", "IR14_done", "IR16_done", "tumour_bam", "normal_bam"]

all_data = {}

test = "Auto_user_OX2-167-TSB_150-Panel_version_1_384_609_IonXpress_014_v1"

#####################################################################################################
# parse the complete list of QUASAR samples ever run 

with open("QUASAR_samples_run_Dec2013.txt") as info:
    for row in info:
        f = row[:-2].split("\t")
        run_id = f[1]

        if not "OX" in run_id: continue
        
        all_data[run_id] = {}
        all_data[run_id]["IR14_done"] = "no_IR_14"
        all_data[run_id]["IR16_done"] = "no_IR_16"
        all_data[run_id]["tumour_bam"] = "no_tumour"
        all_data[run_id]["normal_bam"] = "no_normal"

#####################################################################################################
# parse presence/absence of bams

bam_presence = []

with open("IR_source_files/IonReporter_Sample_Data_14_01_2014.csv") as bam_data:
    for row in bam_data:
        if not "bam" in row: continue
        
        bam_presence.append(row.split(",")[0])
        
# print bam_presence.index("Q2PL2_10C_N_v1")

#####################################################################################################
# parse Tumor/Normal adaptors

adaptors = {}

with open("quasar_tumor_normal_mapping.txt") as adaptor_file:
    for row in adaptor_file:
        f = row[:-2].split("\t")
        
        sample = f[0]
        
        plate = "2" if "PL2" in sample.upper() else "1"
        location = sample.split("_")[1]
        plate_location = (plate, location)
                
        tumornormal = f[1]
        barcode = int(f[2])
        
        if not adaptors.get(plate_location):
            adaptors[plate_location] = {}
        
        adaptors[plate_location][barcode] = tumornormal
        
#####################################################################################################
# parse complete information about the samples

with open("ir_info.csv") as info:
    for row in info:
        if not row.startswith("Q"): continue
         
        f = row[:-2].split(",")
        run_id = f[1]
         
        if not "OX1-127" in run_id: continue
        
        # parse columns into all_data
        for key, value in zip(spreadsheet_header, f):
            if key in output_header:
                all_data[run_id][key] = value
         
        for key in output_header:
            if key not in all_data[f[1]]:
                all_data[run_id][key] = "-"
         
        # check if analysis was done
        if "1.4" in row:
            all_data[run_id]["IR14_done"] = "IR14"
        elif "1.6" in row:
            all_data[run_id]["IR16_done"] = "IR16"
        
        ###############################################################################################
        # FIRST, try to find the names of the Tumor/Normal samples if they are not already collected
        # SECOND, check if a bam file exists in IR with that name
         
        # manually enter tumour and normal if no analysis information is present for this sample
        # if this is not done the tumor/normal name for unanalyzed samples is not logged, 
        # and thus the bam is not accepted even if present
        
        IR_sample = all_data[run_id]["IR_sample"]
        Lab_sample = all_data[run_id]["Lab_Sample"]
        
        if "VCF" in IR_sample: continue
        
        plate = "2" if "PL2" in Lab_sample.upper() else "1"
        location = Lab_sample.replace("-", "_").split("_")[1][:3] # to only keep "A01" as location and remove e.g. "rpt"
        location = location.strip("NT-_")
        plate_location = (plate, location)
        
        for barcode, tumornormal in adaptors[plate_location].iteritems():
            if tumornormal == "T":
                all_data[run_id]["Tumour_Barcode"] = barcode
            else:
                all_data[run_id]["Normal_Barcode"] = barcode

        
        if "IonXpress" in IR_sample: # unanalyzed samplename that doesnt contain "_N_" or "_T_"
                        
            barcode = int(IR_sample.split("_")[-2])
            tumor_normal = adaptors[plate_location][barcode]
            
            if tumor_normal == "T":
                all_data[run_id]["Tumour_Sample"] = IR_sample
            if tumor_normal == "N":
                all_data[run_id]["Normal_Sample"] = IR_sample
            
        else:   
            # FIRST, if theres a "T_" or a "N_" in the samplename
            if "VCF" not in IR_sample:
                if all_data[run_id]["Tumour_Sample"] == "-" and "_T_" in IR_sample:
                   all_data[run_id]["Tumour_Sample"] = IR_sample
        
                if all_data[run_id]["Normal_Sample"] == "-" and "_N_" in IR_sample:
                   all_data[run_id]["Normal_Sample"] = IR_sample           
            
            # FIRST, if the samplename is of the "Autoupload.." format, check in the barcode file
            
            if IR_sample in adaptors.keys():
                if adaptors[IR_sample] == "T":
                    all_data[run_id]["Tumour_Sample"] = IR_sample
                else:
                    all_data[run_id]["Normal_Sample"] = IR_sample

        ###############################################################################################
        # SECOND, check if the Tumor/Normal samplenames have an associated bam 
                
        if all_data[run_id]["Tumour_Sample"] != "-":  
            for bam in bam_presence:
                if all_data[run_id]["Tumour_Sample"] in bam:
                    all_data[run_id]["tumour_bam"] = "tumour_bam"
#                     print "loc", Lab_sample, bam
         
        if all_data[run_id]["Normal_Sample"] != "-":      
            for bam in bam_presence:
                if all_data[run_id]["Normal_Sample"] in bam:
                    all_data[run_id]["normal_bam"] = "normal_bam"
#                     print "loc", Lab_sample, bam
                                                                
        
        print pprint.pprint(all_data[run_id])    

#####################################################################################################

# print "################################"
# print "############ REPORT #############"
# print "################################"

print "\t".join(output_header)

samples = all_data.keys()
samples.sort(cmp=sorter)

for sample in samples:
    output = [sample,]
    
    if "Lab_Sample" in all_data[sample]:
        output.extend([all_data[sample][x] for x in output_header])
    else:
        output.append("missing")
    
    print "\t".join([str(x) for x in output])
    
# pprint.pprint(all_data)            

             
             
             
        
        