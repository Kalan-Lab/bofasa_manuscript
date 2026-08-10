import os
import sys
import pyhmmer

db_file = 'Reitz_etal_2026.hmm'
z = 23
cpus = 50

hmm_lengths = {}
try:
    with pyhmmer.plan7.HMMFile(db_file) as hmm_file:
        for hmm in hmm_file:
            hmm_lengths[hmm.name] = len(hmm.consensus)
except:
    raise RuntimeError("Problem getting HMM consensus lengths!")

protein_faa = 'All_Proteins.faa'
annotation_result_file = 'Metallophore_Search_Results.txt'

try:
    alphabet = pyhmmer.easel.Alphabet.amino()
    sequences = []
    with pyhmmer.easel.SequenceFile(protein_faa, digital=True, alphabet=alphabet) as seq_file:
        sequences = list(seq_file)

        outf = open(annotation_result_file, 'w')
        with pyhmmer.plan7.HMMFile(db_file) as hmm_file:
            for hits in pyhmmer.hmmsearch(hmm_file, sequences, Z=int(z), cpus=cpus):
                for hit in hits:
                    for dom in hit.domains.included:
                        outf.write('\t'.join([hits.query.name.decode(), hit.name.decode(), str(hit.score), str(dom.score)]) + '\n')
        outf.close()
except:
    raise RuntimeError('Problem running pyhmmer!')

