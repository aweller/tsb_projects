

locations = {}
gene_sizes =  {}


with open("human_gene_locations.txt") as loc_file:
    for row in loc_file:
        
        if "Name" in row: continue
         
        f = row.split()
        chr = "chr" + f[0]
        start = int(f[1])
        stop = int(f[2])

        gene = f[3]
                 
        if not locations.get(chr):
           locations[chr] = []
        
        locations[chr].append([start, stop, gene])
        gene_sizes[gene] = 0

gene_sizes["NA"] = 0

# with open("150_gene_panel_gene_locations.txt") as loc_file:
#     for row in loc_file:
#          
#         f = row.split()
#         chr = f[0]
#         pos = int(f[1])
#         gene = f[2].split(":")[0]
#          
#         if not locations.get(chr):
#            locations[chr] = {}
#             
#         locations[chr][pos] = gene
#         gene_sizes[gene] = 0
# 
# gene_sizes["NA"] = 0

last_start = 0
last_stop = 0
last_chr = None

with open("quasar_hotspots.bed") as bed:
    for row in bed:
        if "IAD27482_Designed" in row: continue
        
        f = row.split()
        chr = f[0]
        start = f[1]
        stop = f[2]
        size = int(stop) - int(start)
        gene = "NA"
        
        if chr == last_chr:
            diff = int(last_stop) - int(start)
            if diff > 0:
                size = size - diff
        
        for i in range(int(start), int(stop)):
            for gene_interval in locations[chr]:
            
                if gene_interval[0] <= i <= gene_interval[1]:
                    gene = gene_interval[2]
                    break
            
#         if gene == "NA":
#             print row,
         
        gene_sizes[gene] += size
                     
        last_start = start
        last_stop = stop
        last_chr = chr
        
for gene, size in gene_sizes.iteritems():
    print gene, size
        