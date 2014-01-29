'''
Created Jan 2013

IRAPiUtilities

@author: Joe Wood

'''

import urllib2
import urllib
import logging
import zipfile
import csv
import re
import os
import base64

class IRApiUtilities:
    '''
    classdocs
    '''

    def __init__(self,container_id=None,sample_T_id=None,sample_N_id=None):
        '''
        Constructor
        '''
        self.container_id = container_id
        self.sample_T_id = sample_T_id
        self.sample_N_id = sample_N_id
    
    def get_variome(self,analysis_id,token,analysis_base_url,variome_base_url,output_dir):
    
        #get analysis zip file
        analysis_zipfile = self.get_api_zip(analysis_id,token,analysis_base_url,output_dir)
        
        if(analysis_zipfile != 0):
        
            analysis_z = zipfile.ZipFile(analysis_zipfile.name)
            
            logging.info('Extracting zip file %s',analysis_zipfile.name)
        
            try:
                container_file = analysis_z.extract(analysis_z.namelist()[0],output_dir)
            
                try:
                    container_reader = csv.reader(open(container_file, 'rb'), delimiter='\t')
                
                    rows = list(container_reader)
                    
                    self.container_id = rows[3][0]
                    
                    logging.debug("Container id is %s",self.container_id)
                    
                    #get sample ids for current analysis
                    self.set_sample_ids(rows[3][12])
                    
                    logging.info("Tumour sample id is %s",self.sample_T_id)
                    logging.info("Normal sample_id is %s",self.sample_N_id)
                
                except IOError:
                    print "Error: can\'t find file or read data"
    
            except zipfile.BadZipfile:
                logging.error("Zip file error")
        
            analysis_z.close()
       
            #get variome zip file
            variome_zipfile = self.get_api_zip(self.container_id,self.container_id,token,variome_base_url,output_dir)
            
            if(variome_zipfile != 0):
                variome_z = zipfile.ZipFile(variome_zipfile.name)
            
                logging.debug('Extracting zip file %s',variome_zipfile.name)
            
                try:
                    #extract files
                    variome_z.extractall(output_dir)
                
                except zipfile.BadZipfile:
                    logging.error("Zip file error")
            
                logging.debug('Extraction complete')
            
                variome_z.close()
                #rename files with sample ids
                if (os.path.exists(output_dir+'Sample 1.vcf')):
                    os.rename(output_dir+'Sample 1.vcf', output_dir+self.sample_T_id+'.vcf')
                if (os.path.exists(output_dir+'Sample 1.tsv')):
                    os.rename(output_dir+'Sample 1.tsv', output_dir+self.sample_T_id+'.tsv')
                if (os.path.exists(output_dir+'Sample 2.vcf')):
                    os.rename(output_dir+'Sample 2.vcf', output_dir+self.sample_N_id+'.vcf')
                if (os.path.exists(output_dir+'Sample 2.tsv')):
                    os.rename(output_dir+'Sample 2.tsv', output_dir+self.sample_N_id+'.tsv')
                #reset class variables        
                self.container_id = None
                self.sample_T_id = None
                self.sample_N_id = None    
                return 1
            else:
                #reset class variables        
                self.container_id = None
                self.sample_T_id = None
                self.sample_N_id = None 
                return 0
        else:
            #reset class variables        
            self.container_id = None
            self.sample_T_id = None
            self.sample_N_id = None 
            return 0  
        
    def get_api_zip(self,analysis_id,file_name,token,base_url,output_dir):              
        
        #send request with authentication token (as used in IonReporterUploader plugin)
        req = urllib2.Request(base_url+analysis_id)
        req.add_header("Authorization",token)
        
        zip_filename = output_dir+file_name+".zip"
         
        try:
            f = urllib2.urlopen(req)
            
            logging.debug('Starting file download %s',zip_filename)
            
            # Open local file for writing
            with open(zip_filename, "wb") as local_file:
                local_file.write(f.read())
                
            logging.debug('Completed file download %s',zip_filename)
            
            return local_file
            
        except urllib2.HTTPError, e:
            logging.error('HTTP error: %d',e.code)
            return 0;
        except urllib2.URLError, e:
            logging.error('Network error: %s',e.reason.args[0]+" "+e.reason.args[1])
            return 0;

    def set_sample_ids(self,sample_string):
        
        #logging.debug(sample_string)
        #split out samples
        samples = sample_string.split(';')
        
        #Note order samples returned in can vary eg. T/N or N/T
        for sample in samples:
            sample_info = sample.split('=')
            match = re.search(r'Normal|Self|Tumor', sample_info[0])
            if ((match != None) and (match.group() == 'Normal')):
                self.sample_N_id = sample_info[1]
            elif((match != None) and ((match.group() == 'Tumor') or (match.group() == 'Self'))):
                self.sample_T_id = sample_info[1]
            else:
                logging.error("No sample id")      
                         
#    def get_api_json(self,search_url,token,base_url,output_dir):              
#        
#        #send request with authentication token (as used in IonReporterUploader plugin)
#        req = urllib2.Request(base_url+search_url)
#        data = urllib.urlencode({'name':'/shared/grdata/Oxford_Cancer_and_Haematology_Centre/data/2013-6-25_4_50_36/v2/G151168_v2/IonXpress_009_rawlib.basecaller.bam'})
#        print base_url+search_url
#        req.add_header("Authorization",token)
#        
#        return_filename = output_dir+"outputbam.zip"
#        try:
#            f = urllib2.urlopen(req,data)
#            print req.get_data()
#            logging.debug('Starting file download %s',return_filename)
#            
#            # Open local file for writing
#            with open(return_filename, "wb") as local_file:
#                local_file.write(f.read())
#                
#            logging.debug('Completed file download %s',return_filename)
#            
#            return local_file
#            
#        except urllib2.HTTPError, e:
#            logging.error('HTTP error: %d',e.code)
#            return 0;
#        except urllib2.URLError, e:
#            logging.error('Network error: %s',e.reason.args[0]+" "+e.reason.args[1])
#            return 0;
        
    def get_api_json(self,search_url,url_data,token,base_url,output_dir):              
        
        #send request with authentication token (as used in IonReporterUploader plugin)
        req = urllib2.Request(base_url+search_url)
        data = urllib.urlencode(url_data)
        print base_url+search_url
        req.add_header("Authorization",token)
        
        return_filename = output_dir+re.sub(".json/","", search_url, 0)+".json"
        
        try:
            f = urllib2.urlopen(req,data)
            logging.debug("request data: %s",req.get_data())
            logging.debug('Starting json file download %s',return_filename)
            
            # Open local file for writing
            with open(return_filename, "wb") as local_file:
                local_file.write(f.read())
                
            logging.debug('Completed json file download %s',return_filename)
            
            local_file.close()
            return local_file
            
        except urllib2.HTTPError, e:
            logging.error('HTTP error: %d',e.code)
            return 0;
        except urllib2.URLError, e:
            logging.error('Network error: %s',e.reason.args[0]+" "+e.reason.args[1])
            return 0;
        
    def get_analysis_details(self,analysis_zipfile,ir_version,analysis_summary_filename,output_dir):
        
        analysis_z = zipfile.ZipFile(analysis_zipfile.name)
            
        logging.info('Extracting zip file %s',analysis_zipfile.name)
        
        try:
            
            container_file = analysis_z.extract(analysis_z.namelist()[0],output_dir)
            
            try:
                
                # Open local file for writing
                analysisWriter = open(output_dir+analysis_summary_filename, "wb")
                
                analysisWriter.write("IR_Version,Tumour_Sample,Normal_Sample,Analysis_Name,"+
                                    "Workflow,User,Date\n")
                    
                container_reader = csv.reader(open(container_file, 'rb'), delimiter='\t')
                
                #rows = list(container_reader)
                
                for row in container_reader:
                #logging.debug(', '.join(row))
                    regex = re.compile("Analysis Name:")
                    if row:
                        if regex.match(row[0]):
                            analysis_name_row = re.split(": ", row[0])
                            #logging.debug(analysis_name_row[1])
                            
                            #get analysis info row
                            info_row = container_reader.next()
                            
                            #get sample ids for current analysis
                            self.set_sample_ids(info_row[12])
                            
                            if self.sample_T_id is None:
                                self.sample_T_id = ""
                            if self.sample_N_id is None:
                                self.sample_N_id = ""
                                
                            analysisWriter.write(ir_version+",")
                            analysisWriter.write(self.sample_T_id+",")
                            analysisWriter.write(self.sample_N_id+",")
                            analysisWriter.write(analysis_name_row[1]+",")
                            analysisWriter.write(info_row[4]+",")
                            analysisWriter.write(info_row[9]+",")
                            analysisWriter.write(info_row[10]+"\n")
                    #reset class variables        
                    self.sample_T_id = None
                    self.sample_N_id = None        
            except IOError:
                print "Error: can\'t find file or read data"
    
        except zipfile.BadZipfile:
                logging.error("Zip file error")
        
        analysis_z.close()
        analysisWriter.close()
        
        #return local_file
