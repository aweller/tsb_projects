'''
Created on 20 Apr 2012

@author: wooda1

'''
from config import ir_info_config
from config import manual_match

import csv
import re
import logging


def main():
  
    #configure logging 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    filename=ir_info_config['log_file'],
                    filemode='w') 
    
    #get file contents
    input_samples = open(ir_info_config['sample_list']).readlines()
    ir_samples = open(ir_info_config['ir_sample_file'], 'rb').readlines()
    ir_14_analyses = open(ir_info_config['ir14_analysis_file'], 'rb').readlines()
    ir_16_analyses = open(ir_info_config['ir16_analysis_file'], 'rb').readlines()
    
    #set up output file
    sample_info_file = file(ir_info_config['output_file'], 'wb') 
    
    #set heading
    sample_info_file.write(("Lab_Sample,Run,IR_sample,IR_filetype,"
                            +"IR_Version,Tumour_Sample,Normal_Sample,"
                            +"Analysis_Name,Workflow,Status,User,Date\n"))
   
    missing_count = 0

    for sample in input_samples:
        
        if "Q" not in sample: continue

        sample_found = 0
        
        sample_info = sample.split(',')
        
        original_sample_id = sample_info[0].rstrip()
        
        run_id = sample_info[2].rstrip()
                
        sample_first, sample_second = split_sample_name(original_sample_id)
        

        for ir_sample in ir_samples:
           
           ir_sample_id = ir_sample.split(',')[0].rstrip()

#                match = regex.search(ir_sample_id)
#                run_match = run_regex.search(ir_sample_id)
           
           samplename_match = all([sample_first in ir_sample_id, sample_second in ir_sample_id])
           run_id_match = run_id in ir_sample_id
           
           if (samplename_match or run_id_match):    
#                    print ir_sample
                  
               #logging.debug(match.group()+","+ir_sample_id)
                
               sample_found = 1
                
               #find analysis with ir_sample_id
               #IR 1.4
               ir_14_analysis_list = get_ir_analyses(ir_sample_id,ir_14_analyses)
               #IR 1.6
               ir_16_analysis_list = get_ir_analyses(ir_sample_id,ir_16_analyses)
               
               #logging.debug(len(ir_14_analysis_list))
               #logging.debug(len(ir_16_analysis_list))
                               
               if re.search("sff",ir_sample.split(',')[2],re.IGNORECASE):
                    sample_info_str = original_sample_id+","+run_id+","+ir_sample_id+",sff,"
               elif re.search("vcf",ir_sample.split(',')[2],re.IGNORECASE):
                    sample_info_str = original_sample_id+","+run_id+","+ir_sample_id+",vcf,"
               else:
                    sample_info_str = original_sample_id+","+run_id+","+ir_sample_id+",bam,"
                
               if not ((len(ir_14_analysis_list)==0) and (len(ir_16_analysis_list)==0)):
                    #print sample info and all analyses
                    for ir_14_analysis in ir_14_analysis_list:
                    
                        sample_info_file.write(sample_info_str)
                    
                        ir_14_analysis_info = ir_14_analysis.split(',')
                    
                        analysis_info_len = len(ir_14_analysis_info)
                    
                        for idx,info_item in enumerate(ir_14_analysis_info):
                            if idx==(analysis_info_len-1):
                                sample_info_file.write(info_item)
                            else:
                                sample_info_file.write(info_item+",")
                
                    for ir_16_analysis in ir_16_analysis_list:
                    
                        sample_info_file.write(sample_info_str)
                    
                        ir_16_analysis_info = ir_16_analysis.split(',')
                    
                        analysis_info_len = len(ir_16_analysis_info)
                    
                        for idx,info_item in enumerate(ir_16_analysis_info):
                            if idx==(analysis_info_len-1):
                                sample_info_file.write(info_item)
                            else:
                                sample_info_file.write(info_item+",")               
               else:
                   sample_info_file.write(sample_info_str+"\n")                     
         
        if(sample_found == 0):
               
           if manual_match.get(original_sample_id):
               sample_found = 1
               sample_status = manual_match[original_sample_id]
              
               logging.debug(original_sample_id+","+run_id+","+sample_status)   
               sample_info_file.write(original_sample_id+","+run_id+","+sample_status+"\n")
               
           else:    
               print "----"
               print sample, run_id, original_sample_id, sample_first, sample_second
                               
               missing_count += 1
                
               #logging.debug(original_sample_id+",No Match,"+sample_id) 
               logging.debug(original_sample_id+","+run_id+",No Match") 
                
               sample_info_file.write(original_sample_id+","+run_id+",No Match\n")
                
               
                 
    
    sample_info_file.close()           
    logging.info('missing count %s',missing_count)
    logging.info('finished')

def get_ir_analyses(sample_id,analyses):

    sample_analyses = []
    
    for analysis in analyses:
        analysis_info = analysis.split(',')
        if sample_id in (analysis_info[1],analysis_info[2]):
            #add line to sample_analyses
            sample_analyses.append(analysis)
    
    return sample_analyses

def split_sample_name(original_sample_id):

    samples_parts = original_sample_id.replace("VICTORindels","indel").replace("-", "_").split("_")
    
    if len(samples_parts) < 2:
        if "VICTOR" in original_sample_id:
            sample_first = "VICTOR"
            sample_second = original_sample_id[-2:]   

        elif "ENDO" in original_sample_id:
            sample_first = "ENDO"
            sample_second = original_sample_id[4:6]

        elif "CRC" in original_sample_id:
            sample_first = "CRC"
            sample_second = original_sample_id[3:]
        
        else:
            print sample, "too short"
            sample_first, sample_second = None, None
    else:
        sample_first = samples_parts[0]
        sample_second = samples_parts[1][:3] 
        
    return sample_first, sample_second

# def modify_sample_id(sample_id):
#       
#       new_sample_id = sample_id
#       
#       #change victor indel strings 
#       vicindel_samples = get_bad_samples('VICindel_')
#       
#       for vicindel_sample in vicindel_samples:
#           if (vicindel_sample == new_sample_id):
#               new_sample_id = new_sample_id.replace("VICTORindels-","VICindel_")
#       
#       vicindel_samples = get_bad_samples('VICindel-')
#       
#       for vicindel_sample in vicindel_samples:
#           if (vicindel_sample == new_sample_id):
#               new_sample_id = new_sample_id.replace("VICTORindels","VICindel")
#       
#       vicindel_samples = get_bad_samples('VICTORindels_bracket')
#       
#       for vicindel_sample in vicindel_samples:
#           if (vicindel_sample == new_sample_id):
#               new_sample_id = new_sample_id.replace("VICTORindels-","VICTORindels_")
#               new_sample_id = re.sub('\(.*\)','',new_sample_id)
#               #logging.debug("BRACKETS GONE! %s",new_sample_id)
#               return new_sample_id
#              
#       regex = re.compile("VICTORindels")
#       match = regex.search(new_sample_id)
#       
#       if match:
#           #logging.debug("MATCH! "+match.group())
#           new_sample_id = new_sample_id.replace("VICTORindels","VICindels")
#           new_sample_id = new_sample_id.replace("-","_")
#           #logging.debug(new_sample_id)
#       
#       #S.Am samples - to _
#       regex = re.compile("S.Am")
#       match = regex.search(new_sample_id)
#       if match:
#           #logging.debug("MATCH! "+match.group())
#           new_sample_id = new_sample_id.replace("-","_")
#           #logging.debug(new_sample_id)
#       
#       #Quasar complete name
#       regex = re.compile("QUASAR2pl1")
#       match = regex.search(new_sample_id)
#       if match:
#           #logging.debug("MATCH! "+match.group())
#           new_sample_id = new_sample_id.replace("r","QUASAR2pl1")
#           #logging.debug(new_sample_id)
#       
#       #Quasar remove rpt text
#       regex = re.compile("QUASAR2pl1")
#       match = regex.search(new_sample_id)
#       if match:
#           #logging.debug("MATCH! "+match.group())
#           new_sample_id = new_sample_id.replace("r","")
#           new_sample_id = new_sample_id.replace("rpt","")
#           #logging.debug(new_sample_id)
# 
#       
#       return new_sample_id 
# 
# def get_bad_samples(bad_type):
#     
#     bad_samples = []
# 
#     if(bad_type == 'VICindel_'):
#         bad_samples = [
#                         "VICTORindels-7G",
#                         "VICTORindels-7H",
#                         "VICTORindels-8A",
#                         "VICTORindels-8B",
#                         "VICTORindels-8C",
#                         "VICTORindels-8D",
#                         "VICTORindels-8F",
#                         "VICTORindels-8G",
#                         "VICTORindels-8H",
#                         "VICTORindels-10C",
#                         "VICTORindels-10D",
#                         "VICTORindels-10E",
#                         "VICTORindels-10F",
#                         "VICTORindels-10G"
#                     ]
#     elif(bad_type == 'VICindel-'):
#         bad_samples = [
#                         "VICTORindels-7C",
#                         "VICTORindels-7D",
#                         "VICTORindels-7E",
#                         "VICTORindels-7F",
#                         "VICTORindels-8E",
#                       ]
#     elif(bad_type == 'VICTORindels_bracket'):
#         bad_samples = [
#                        "VICTORindels-A03(9A)",
#                        "VICTORindels-B03(9B)",
#                        "VICTORindels-C03(9C)",
#                        "VICTORindels-D03(9D)",
#                        "VICTORindels-E03(9E)",
#                        "VICTORindels-F03(9F)",
#                        "VICTORindels_G03(9G)",
#                        "VICTORindels-H03(9H)",
#                        "VICTORindels-A04(10A)",
#                        "VICTORindels-B04(10B)"               
#                       ]
#     '''
#     elif(bad_type == 'QUASARrpt'):
#         bad_samples = [
#                        "QUASAR2pl1_B12",
#                        "QUASAR2pl1_C12"
# 
#                       ]
#     '''                           
#     return bad_samples



if __name__ == '__main__':
    main()



    
'''

'''   