'''
Created on 20 Apr 2012

@author: wooda1

'''
from config import genelist_config
import csv
import logging


def main():
  
    #configure logging 
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d-%m-%y %H:%M',
                    filename=genelist_config['log_file'],
                    filemode='w') 
    
    common_genes_file = file(genelist_config['common_genes'], 'w') 
    unique_genes_file = file(genelist_config['unique_genes'], 'w') 
    
    genelist_one_file = open(genelist_config['genelist_one']).readlines() 
    genelist_two_file = open(genelist_config['genelist_two']).readlines()
    
    for gene in genelist_one_file:
        if gene in genelist_two_file:
            common_genes_file.write(gene)
        else:
            unique_genes_file.write(gene)

    common_genes_file.close() 
    unique_genes_file.close()
    
    logging.info('finished')
       
if __name__ == '__main__':
    main()
    
    