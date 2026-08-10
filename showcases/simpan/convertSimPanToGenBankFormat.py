import os
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from collections import defaultdict

simpan_dir = 'simpan_simulated_dataset/'
gbk_dir = 'Simpan_GBks/'

for f in os.listdir(simpan_dir):
    if f.endswith('.gff') and not f.startswith('.'):
        gff = simpan_dir + f
        fna = simpan_dir + f.split('.gff')[0] + '.fna'
        genome_id = f.split('_')[1].split('.')[0]
        
        seqs = {}
        with open(fna) as of:
            for rec in SeqIO.parse(of, 'fasta'):
                seqs[rec.id] = str(rec.seq)

        gbk = gbk_dir + genome_id + '.gbk'
        outf = open(gbk, 'w')
    
        feature_list = defaultdict(list)

        with open(gff) as og:
            for line in og:
                if line.startswith('#'): continue
                line = line.strip()
                ls = line.split('\t')
                if len(ls) < 6: continue
                if ls[2] != 'CDS': continue
                scaff = ls[0]
                start = int(ls[3])
                end = int(ls[4])
                direction = ls[6]
                strand = 1
                if direction == '-':
                    strand = -1
                gene_id = ls[-1].split('locus_tag=')[1].split(';')[0]
                gene_name = genome_id + '|' + gene_id
                
                gene_seq = Seq(seqs[scaff][start-1:end])
                if direction == '-':
                    gene_seq = gene_seq.reverse_complement()

                prot_seq = gene_seq.translate()
         
                feature = SeqFeature(FeatureLocation(start=start-1, end=end, strand=strand), type='CDS')
                feature.qualifiers['locus_tag'] = gene_id
                feature.qualifiers['gene'] = gene_id
                feature.qualifiers['translation'] = prot_seq.rstrip('*')
                feature.qualifiers['product'] = "hypothetical protein"
                feature_list[scaff].append(feature)

        with open(fna) as of:
            for rec in SeqIO.parse(of, 'fasta'):
                seq = rec.seq
                record = SeqRecord(seq, id=rec.id, name=rec.id, description='')
                record.annotations['molecule_type'] = 'DNA'
                record.features = feature_list[rec.id]
                SeqIO.write(record, outf, 'genbank')
        outf.close()
