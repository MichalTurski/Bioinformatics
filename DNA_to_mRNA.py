import re
import sys
import itertools


dna_to_mrna_dict = {'T': 'A', 'A': 'U', 'C': 'G', 'G': 'C'}

amino_acid_to_rna_dict = {'PHE': ('UUU', 'UUC'), 'LEU': ('UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'), 'ILE': ('AUU', 'AUC', 'AUA'), 'MET': ('AUG',), 'VAL': ('GUU', 'GUC', 'GUA', 'GUG'), 'SER': ('UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'), 'PRO': ('CCU', 'CCC', 'CCA', 'CCG'), 'THR': ('ACU', 'ACC', 'ACA', 'ACG'), 'ALA': ('GCU', 'GCC', 'GCA', 'GCG'), 'TYR': ('UAU', 'UAC'), 'STOP': ('UAA', 'UAG', 'UGA'), 'HIS': ('CAU', 'CAC'), 'GLN': ('CAA', 'CAG'), 'ASN': ('AAU', 'AAC'), 'LYS': ('AAA', 'AAG'), 'ASP': ('GAU', 'GAC'), 'GLU': ('GAA', 'GAG'), 'CYS': ('UGU', 'UGC'), 'TRP': ('UGG',), 'ARP': ('CGU', 'CGC', 'CGA', 'CGG'), 'ARG': ('AGA', 'AGG'), 'GLY': ('GGU', 'GGC', 'GGA', 'GGG')}

codon2aa = {"AAA":"K", "AAC":"N", "AAG":"K", "AAU":"N",
                "ACA":"T", "ACC":"T", "ACG":"T", "ACU":"T",
                "AGA":"R", "AGC":"S", "AGG":"R", "AGU":"S",
                "AUA":"I", "AUC":"I", "AUG":"M", "AUU":"I",

                "CAA":"Q", "CAC":"H", "CAG":"Q", "CAU":"H",
                "CCA":"P", "CCC":"P", "CCG":"P", "CCU":"P",
                "CGA":"R", "CGC":"R", "CGG":"R", "CGU":"R",
                "CUA":"L", "CUC":"L", "CUG":"L", "CUU":"L",

                "GAA":"E", "GAC":"D", "GAG":"E", "GAU":"D",
                "GCA":"A", "GCC":"A", "GCG":"A", "GCU":"A",
                "GGA":"G", "GGC":"G", "GGG":"G", "GGU":"G",
                "GUA":"V", "GUC":"V", "GUG":"V", "GUU":"V",

                "UAA":"_", "UAC":"Y", "UAG":"_", "UAU":"T",
                "UCA":"S", "UCC":"S", "UCG":"S", "UCU":"S",
                "UGA":"_", "UGC":"C", "UGG":"W", "UGU":"C",
                "UUA":"L", "UUC":"F", "UUG":"L", "UUU":"F"}



mrna_to_amino_acid_dict = {}
for amino_acid, codons in amino_acid_to_rna_dict.items():
    mrna_to_amino_acid_dict.update(dict.fromkeys(codons, amino_acid))


def dna_to_mrna(dna_sequence):
    dna_sequence = re.sub(r'[^A-Z]', '', dna_sequence.upper())
    mrna_sequence = ''
    for nucleotide in dna_sequence:
        mrna_sequence += dna_to_mrna_dict.get(nucleotide, '?')
    return mrna_sequence


def mrna_to_amino_acid(mrna_sequence):
    mrna_sequence = re.sub(r'[^A-Z]', '', mrna_sequence.upper())
    amino_acid_sequence = []
    while mrna_sequence:
        amino_acid_sequence.append(codon2aa.get(mrna_sequence[:3], '???'))
        mrna_sequence = mrna_sequence[3:]
    return amino_acid_sequence


def count_GC(sequence):
    count_table = []
    while len(sequence) > 100:
        curr_seq = sequence[0:50]
        g_count = curr_seq.count("G")
        c_count = curr_seq.count("C")
        count_table.append(g_count + c_count)
        sequence = sequence[50:]
    return count_table


def main():
    # dna_sequence = ''.join(sys.argv[1:]) or input('Please enter the DNA sequence for conversion: ')
    with open(sys.argv[1], 'r') as file:
        dna_sequence = file.read().replace('\n', '')
    mrna = dna_to_mrna(dna_sequence)
    mrna_sequence = []
    print(count_GC(dna_sequence))
    while mrna:
        mrna_sequence.append(mrna[:3])
        mrna = mrna[3:]
    print('mRNA: {}'.format('-'.join(mrna_sequence)))
    print('Amino acids: {}'.format('-'.join(mrna_to_amino_acid(dna_to_mrna(dna_sequence)))))


if __name__ == "__main__":
    main()
