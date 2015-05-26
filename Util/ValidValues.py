'''
 Here are the dicts of all valid values for the various fields of a HGVS nomenclature.
'''

# valid variant types 
v_types = {'c':'cDNA', 'm':'mRNA', 'g':'genomic', 'p':'protein'}

# operator types
operators = {'dup':'duplicate', 'del':'deletion', 'inv':'inversion', 'con':'conversion', 'ins':'insertion', 'delins':'insertion deletion'}

# valid protein operators
protein_operators = {'del':'deletion', 'ins':'insertion', 'delins':'insertion deletion', '*':'translation termination',
                     '?':'Unkown', 'dup':'duplicate'}

# nucleotides
# I called this part nucleotides but really it can be used for nucleotides or amino acids
# NOTE: although the codes are identicle, the amino acid codes have a complete different meaning
# to nucleotides(See the dict values, aa = amino acid, nt = nucleotides).
nucleotides = { 'a':'adenine', 'c':'cytosine', 'g':'guanine', 't':'thymine',
                'b':'c, g or t', 'd':'a, g or t', 'h':'a, c or t', 'k':'g or t',
                'm':'a or c', 'n':'a, c, g or t', 'r':'a or g', 's':'g or c', 'v':'a, c or g',
                'w':'a or t', 'y':'c or t', '*':'wildcard' }

# amino acids - three char long
amino_acids = { 'ala':'alanine', 'asx':'aspartic acid or asparagine', 'cys':'cysteine', 'asp':'aspartic acid',
                'glu':'glutamic acid', 'phe':'phenylalanine', 'gly':'glycine', 'his':'histidine',
                'ile':'isoleucine', 'lys':'lysine', 'leu':'leucine', 'met':'methionine',
                'asn':'asparagine', 'pro':'proline', 'gln':'glutamine', 'arg':'arginine',
                'ser':'serine', 'thr':'threonine', 'sec':'selenocysteine', 'val':'valine',
                'trp':'tryptophan', 'xaa':'unknown or other', 'tyr':'tyrosine', 'glx':'glutamic acid or glutamine',
                '*':'Termination'
                }

# amino_acids - single char long
amino_acids_single = { 'a':'alanine', 'b':'aspartic acid or asparagine', 'c':'cysteine', 'd':'aspartic acid',
                'e':'glutamic acid', 'f':'phenylalanine', 'g':'glycine', 'h':'histidine',
                'i':'isoleucine', 'k':'lysine', 'l':'leucine', 'm':'methionine',
                'n':'asparagine', 'p':'proline', 'q':'glutamine', 'r':'arginine',
                's':'serine', 't':'threonine', 'u':'selenocysteine', 'v':'valine',
                'w':'tryptophan', 'x':'unknown or other', 'y':'tyrosine', 'z':'glutamic acid or glutamine',
                '*':'Termination'
                }
