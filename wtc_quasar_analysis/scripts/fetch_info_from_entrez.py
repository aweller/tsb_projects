from Bio import Entrez
import sys
Entrez.email = "andreas.m.weller@gmail.com"     # Always tell NCBI who you are


def fetch_gene_position(gene_id):
    
    ##########################################
    # fetch record
#     search_string = gene_id+"[Gene] AND human[Organism]"
    search_string = gene_id+"[Gene/Protein Name] AND human[Organism]"
    
    handle = Entrez.esearch(db="gene", term=search_string)
    record = Entrez.read(handle)
    ids = record['IdList']
    
    if not ids: # no records where found
        return "NA", "NA", "NA" 
    
    seq_id = find_correct_return_field(gene_id, ids)
    
    if seq_id:
        handle = Entrez.efetch(db="gene", id=seq_id, rettype="gene_table", retmode="text")
        record = handle.read()
         
        ##########################################   
        # parse record
         
        fields =  record.split()
         
        record_first_row = record.split("\n")[0]
        record_gene_name = record_first_row.split()[0]
         
#         print gene_id, record_gene_name, seq_id, ids[:6]
         
    #     if record_gene_name != gene_id:
    #         print "Mismatch:", record_gene_name, gene_id
        
        chrom_field = [x for x in fields if x.startswith("NC_")][0]
        chrom_no = chrom_field.split(".")[0][-2:].lstrip("0")
        if chrom_no == "23":
            chrom_no = "X"
        chrom = "chr" + chrom_no
        
        start_index = fields.index("from:") + 1
        start = fields[start_index]
        
        # the stop position is tricky because its sometimes not right after the "to:"
        stop_index = fields.index("to:") + 1
        stop = fields[stop_index]
        stop_found = False
        
        while stop_found == False:
            try:
                stop = int(stop)
                stop = str(stop)
                stop_found = True
            except:
                stop_index += 1
                stop = fields[stop_index]
        
        ##########################################
        # check the strandedness and reverse if needed
        
        if int(stop) < int(start):
            start, stop = stop, start
    
        return chrom, start, stop
    
    else:
#         print "Error for", gene_id
        return "NA","NA","NA" 

def find_correct_return_field(gene_id, ids):
    """ Retrieves records from GeneIDs results and doublechecks if it matches the original query"""
    
    found = False
    
    for id in ids:
        seq_id = id
            
        handle = Entrez.efetch(db="gene", id=seq_id, rettype="gene_table", retmode="text")
        record = handle.read()
        record_first_row = record.split("\n")[0]                
        record_gene_name = record_first_row.split()[0]
        
#         print record_gene_name, gene_id
        
        if record_gene_name.lower() == gene_id.lower():
            found = True
            break
    
    if found:
        return seq_id                
    else:
        return False
    
if __name__ == "__main__":
    gene_id = sys.argv[1]
    print fetch_gene_position(gene_id)