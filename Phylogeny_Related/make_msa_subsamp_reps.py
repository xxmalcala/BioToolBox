#!/usr/bin/env python3

import random, sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def grab_cols(fasta_file, pct, reps = 10):
    seqs = {i.id:f'{i.seq}' for i in SeqIO.parse(fasta_file,'fasta')}
    slen = [n for n in range(len(list(seqs.values())[0]))]
    for n in range(1, reps+1):
        random.shuffle(slen)
        tmp_seqs = []
        for k, v in seqs.items():
            x = ''
            for i in slen[:int(len(slen)/pct)]:
                x += v[i]
            tmp_seqs.append(SeqRecord(Seq(x),k,'',''))
        outfas = f'{fasta_file.split(".fas")[0]}.{pct}pctSites.Rep{n}.fas'
        SeqIO.write(tmp_seqs, outfas, 'fasta')


if __name__ == '__main__':
    if len(sys.argv[1:]) == 1:
        fasta_file = sys.argv[1]
        pct = 10
        reps = 10
    elif len(sys.argv[1:]) == 2:
        fasta_file = sys.argv[1]
        pct = int(sys.argv[2])
        reps = 10
    elif len(sys.argv[1:]) == 3:
        fasta_file = sys.argv[1]
        pct = int(sys.argv[2])
        reps = int(sys.argv[3])
    else:
        print('\nUsage:\n    python3 make_msa_subsamp_reps.py [FASTA-FILE] [PCT-SITES] [NUM-REPS]\n')
        sys.exit()

    grab_cols(fasta_file, pct, reps)
