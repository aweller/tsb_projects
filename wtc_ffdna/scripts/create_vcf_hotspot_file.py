# chr7    55249110        .       G       A       .       .       id=1

def sorter(row1, row2):
    f1 = row1.split("\t")
    f2 = row2.split("\t")
    
    if int(f1[0].lstrip("chr")) > int(f2[0].lstrip("chr")):
        return 1
    elif int(f1[0].lstrip("chr")) < int(f2[0].lstrip("chr")):
        return -1
    
    else:
        if int(f1[1]) > int(f2[1]):
            return 1 
        elif int(f1[1]) < int(f2[1]):
            return -1
        else:
            return 0 

header = """##fileformat=VCFv4.1
##fileDate=20131017
##source=Torrent Unified Variant Caller (Extension of freeBayes)
##reference=/shared/grdata/.reference/hg19_v12/hg19.fasta
##reference=file:///shared/grdata/.reference/hg19_v12/hg19.fasta
##contig=<ID=chr1,length=249250621,assembly=hg19>
##contig=<ID=chr10,length=135534747,assembly=hg19>
##contig=<ID=chr11,length=135006516,assembly=hg19>
##contig=<ID=chr12,length=133851895,assembly=hg19>
##contig=<ID=chr13,length=115169878,assembly=hg19>
##contig=<ID=chr14,length=107349540,assembly=hg19>
##contig=<ID=chr15,length=102531392,assembly=hg19>
##contig=<ID=chr16,length=90354753,assembly=hg19>
##contig=<ID=chr17,length=81195210,assembly=hg19>
##contig=<ID=chr18,length=78077248,assembly=hg19>
##contig=<ID=chr19,length=59128983,assembly=hg19>
##contig=<ID=chr2,length=243199373,assembly=hg19>
##contig=<ID=chr20,length=63025520,assembly=hg19>
##contig=<ID=chr21,length=48129895,assembly=hg19>
##contig=<ID=chr22,length=51304566,assembly=hg19>
##contig=<ID=chr3,length=198022430,assembly=hg19>
##contig=<ID=chr4,length=191154276,assembly=hg19>
##contig=<ID=chr5,length=180915260,assembly=hg19>
##contig=<ID=chr6,length=171115067,assembly=hg19>
##contig=<ID=chr7,length=159138663,assembly=hg19>
##contig=<ID=chr8,length=146364022,assembly=hg19>
##contig=<ID=chr9,length=141213431,assembly=hg19>
##contig=<ID=chrM,length=16569,assembly=hg19>
##contig=<ID=chrX,length=155270560,assembly=hg19>
##contig=<ID=chrY,length=59373566,assembly=hg19>"""
    
    

genes =     ["KRAS","EGFR", "KRAS","EGFR","BRAF","KRAS","EGFR","BRAF","KRAS","EGFR","PIK3CA"]
chroms = [12, 7, 12, 7, 7, 12, 7,7,12,7,3]
positions = [25398284,55242468,25398285,55249071,140453137,25398284,55259515,140453136,25398281,55242465,178936091]
nt_change = ["c.35G>C","ATTAAGAGAAGCAACATCT/ATTAAGAGAAGCAACATCT>A","c.34G>T","c.2369C>T","c.1798_1799GT>AA","c.35G>T","c.2573T>G","c.1799T>A","c.38G>A","GGAATTAAGAGAAGCAACATCT/GGAATTAAGAGAAGCAACATCT>G","c.1633G>A"]
ff_strand_nt_change = ["C>G","ATTAAGAGAAGCAACATCT>A","C>A","C>T","C>T","C>A","T>G","A>T","C>T","GGAATTAAGA>G","G>A"]

rows = []

for i in range(len(genes)):
    
    gene = genes[i]
    pos = str(positions[i])
    chrom = "chr"+str(chroms[i])
    ref = ff_strand_nt_change[i].split(">")[0]
    alt = ff_strand_nt_change[i].split(">")[1]
    dot = "."
    
    info = ";".join([gene, ff_strand_nt_change[i]])
    
    row = "\t".join([chrom, pos, dot, ref, alt, dot, dot, info])
    rows.append(row)

print header
rows.sort(cmp=sorter)
for row in rows:
    print row