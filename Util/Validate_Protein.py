from Util import get_value
from Util import get_operator
from Util import check_numeric_value
from Util import get_repeater_value
from Util import split
import ValidValues

def validate(variant): 
    # Please not that since protein nomenclature is different to genomic/cDNA structure the values are
    # stored differently in the VariantName Class.
    # Since the protein positions and ranges contain the amino acid and numeric value for the index
    # of that amino acid the variant position, range_lower and range_upper  will store the amino acids
    # while the intron fields will store the index.

    # position: amino acid
    if variant.position.strip() != '':
        if variant.position not in ('?', '='):
            if not variant.position.lower() in ValidValues.amino_acids:
                if not variant.position.lower() in ValidValues.amino_acids_single:
                    return False
        else:
            return True

    # position: index of the amino acid 
    if variant.position_intron.strip() != '':
        # if position has a value then intron should too
        if variant.position.strip() != '':
            if not check_numeric_value(variant.position_intron):
                return False
        else:
            return False

    # range_lower: amino acid
    if variant.range_lower.strip() != '':
        if variant.position.strip() == '':
            if not variant.range_lower.lower() in ValidValues.amino_acids:
                return False
        else:
            return False

    # range_lower: index of the amino acid
    if variant.range_lower_intron.strip() != '':
        if variant.range_lower.strip() != '':
            if not check_numeric_value(variant.range_lower_intron):
                return False
        else:
            return False

    # range_upper: amino acid
    if variant.range_upper.strip() != '':
        if variant.range_lower.strip() != '':
            if not variant.range_upper.lower() in ValidValues.amino_acids:
                return False
        else:
            return False

    # range_upper: index of the amino acid
    if variant.range_upper_intron.strip() != '':
        if variant.range_upper.strip() != '':
            if not check_numeric_value(variant.range_upper_intron):
                return False
        else:
            return False
    
    # Operator
    if variant.operator.strip() != '':
        # check for repeating range
        if not variant.operator[0] != '(' or not variant.operator[0] != '[':
            if not get_repeater_value(variant.operator):
                return False
        # check for indels --> 'delins' and insertions --> 'ins'
        elif variant.operator.lower() not in ValidValues.protein_operators:
            # check for amino acids
            if not variant.operator.lower() in ValidValues.amino_acids:
                if not variant.operator.lower() in ValidValues.amino_acids_single:
                    return False
    else:
        return False

    # Operator Value: should only contain amino acids for indel and insertion
    # operators. 
    if variant.operator_value.strip() != '':
        # frameshifts        
        if variant.operator_value[0:2] == 'fs':
            if len(variant.operator_value) > 2:
                if variant.operator_value[2].lower() in ('*', 'x'):
					# check for '];['
                    if '];[' in variant.operator_value[3:]:
                        p = variant.operator_value.index('];[')
                        if variant.operator_value[3:p] != '':
                            if not variant.operator_value[3:p].isdigit():
                                return False
                    else:                        
                        if not variant.operator_value[3:].isdigit():
                            return False
                else:
                    return False
        else:
            # ignore if operator begins with ']' or ')'
            if ']' not in variant.operator_value and ')' not in variant.operator_value:
                # operator value can not be empty if the operator is an indel or insertion
                if variant.operator.lower() not in ValidValues.protein_operators:
                    # The length of operator string should be divisble by 3 since the amino acid
                    # codes should only be 3 chars long.
                    if not len(variant.operator_value) % 3 != 0:
                        return False
                    else:
                        # need to check each amino acid if valid
                        amino_acids = split(variant.operator_value.lower(), 3)
                        for amino_acid in amino_acids:
                            item_found = False
                            if amino_acid in ValidValues.amino_acids:
                                item_found = True
                            # if amino acid not found
                            if not item_found:
                                return False
        
    return True
