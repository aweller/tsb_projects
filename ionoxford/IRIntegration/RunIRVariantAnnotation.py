'''
Created Dec 2012

RunIRVariantAnnotation

@author: Joe Wood

'''

import logging
from config import api_config
import IRApiUtilities
import csv

def main():
    
    #configure logging 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    filename=api_config['log_file'],
                    filemode='w') 
       
    myIRApiUtilities = IRApiUtilities.IRApiUtilities()
    
    #Read analysis.csv file
    try:
        analysisReader = csv.reader(open(api_config['analysis_file'], 'rb'), delimiter=',')
    except IOError:
        print "Error: can\'t find file or read data"
        logging.error("Error: can\'t find file or read data")
        
    logging.debug('analysis_file %s read',api_config['analysis_file']) 
    
    #Get variome files    
    for analysis_id in analysisReader:
        
        get_variome = myIRApiUtilities.get_variome(analysis_id[0],api_config['token'],api_config['analysis_base_url'],api_config['variome_base_url'],api_config['output_path'])
        
        if(get_variome == 1):
            logging.info('Variome exported for analysis %s',analysis_id[0])
        elif(get_variome == 0):
            logging.error('Variome export failed for analysis %s',analysis_id[0])
    
    logging.info("Finished")    

if __name__ == '__main__':
    main()