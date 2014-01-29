'''
Created July 2013

RunIRSampleDataExport

@author: Joe Wood

'''

import logging
from config import api_config
import IRApiUtilities
import csv
import json
import Model.SampleIR as SampleIR
import re


def main():
    
    #configure logging 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    filename=api_config['log_file'],
                    filemode='w') 
       
    myIRApiUtilities = IRApiUtilities.IRApiUtilities()
    
    
    try:
        sampleReader = csv.reader(open(api_config['sample_file'], 'rb'), delimiter=',')
    except IOError:
        print "Error: can\'t find file or read data"
        logging.error("Error: can\'t find file or read data")
        
    logging.debug('sample_file %s read',api_config['sample_file']) 
    
    #Get a sample json file
    for sample_id in sampleReader:
     
       url_data={'name':sample_id[0]}
       search_url="samples.json/"
       sample_json_file = myIRApiUtilities.get_api_json(search_url,url_data,api_config['token'],api_config['rest_base_url'],api_config['output_path'])
       
       sample_json = json.load(open(sample_json_file.name,'r'))
       
       sample_ir = SampleIR.SampleIR(sample_json)
       
       print sample_ir.name
       print sample_ir.barCode[0]
       print re.split("=",sample_ir.analysisDetails[0]['ir14']['analysis_url_1'])[1]
       print sample_ir.data_links
       

       sample_json_file.close();
    
    logging.info("Finished")    

if __name__ == '__main__':
    main()