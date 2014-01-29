import fetch_info_from_entrez as fetch
import sys

input_file = sys.argv[1]

with open(input_file) as input:
    for row in input:
        
        f = row.split()
        
        gene_id = f[0]
        
#         if gene_id[0] != "P" : continue
        
        if gene_id == "EML4-ALK":
            gene_id = "EML4"
            chrom, start, stop = fetch.fetch_gene_position(gene_id) 
            print "\t".join([chrom, start, stop, "EML4(fusion)"])

            gene_id = "ALK"
            chrom, start, stop = fetch.fetch_gene_position(gene_id) 
            print "\t".join([chrom, start, stop, "ALK(fusion)"])
        
        elif gene_id == "TNKS1":
            gene_id = "TNKS"
            chrom, start, stop = fetch.fetch_gene_position(gene_id) 
            print "\t".join([chrom, start, stop, "TNKS1"])
            
        else:
        
            chrom, start, stop = fetch.fetch_gene_position(gene_id) 
            print "\t".join([chrom, start, stop, gene_id])
