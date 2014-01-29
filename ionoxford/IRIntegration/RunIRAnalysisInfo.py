'''
Created Oct 2013

RunIRAnalysisInfo

@author: Joe Wood

'''

import logging
from config import api_config
import IRApiUtilities
import csv
import urllib2
import urllib

def main():
    
    #configure logging 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    filename=api_config['log_file'],
                    filemode='w') 
       
    myIRApiUtilities = IRApiUtilities.IRApiUtilities()
    
    #get all analyses metadata files
    
    #1.4 Ion Reporter
    ir14_file = myIRApiUtilities.get_api_zip("","all_analyses_14",api_config['token'],api_config['all_analysis_14_base_url'],
                                 api_config['output_path'])    
    
    #1.6 Ion Reporter
    ir16_file = myIRApiUtilities.get_api_zip("","all_analyses_16",api_config['token'],api_config['all_analysis_16_base_url'],
                                 api_config['output_path'])    

    myIRApiUtilities.get_analysis_details(ir14_file,"1.4",api_config['analysis_summary_filename']+"_14.csv",api_config['output_path'])
    
    myIRApiUtilities.get_analysis_details(ir16_file,"1.6",api_config['analysis_summary_filename']+"_16.csv",api_config['output_path'])
    
    
    logging.info("Finished")    

if __name__ == '__main__':
    main()