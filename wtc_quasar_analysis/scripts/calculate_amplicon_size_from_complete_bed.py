
gene_sizes =  {}

last_start = 0
last_stop = 0
last_chr = None

with open("../data/genepanel_148_amplicons_and_genes.bed") as bed:
    for row in bed:
        if "IAD27482_Designed" in row: continue
        
        f = row.split()
        chr = f[0]
        start = f[1]
        stop = f[2]
        size = int(stop) - int(start)
        gene = f[4]
        
        if chr == last_chr:
            diff = int(last_stop) - int(start)
            if diff > 0:
                size = size - diff
        
        if not gene_sizes.get(gene):
            gene_sizes[gene] = 0
            
        gene_sizes[gene] += size
                     
        last_start = start
        last_stop = stop
        last_chr = chr
        
for gene, size in gene_sizes.iteritems():
    print gene, size
        

