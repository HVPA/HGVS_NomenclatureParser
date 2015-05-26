from Variant import VariantName
from Util import get_value
from Util import get_operator
from Util import check_numeric_value
from ValidValues import amino_acids

def parser(variant_string, variant): 
    # for amino acids only the 3 char is acceptable which is the preferred method
    # according to HGVS. eg: For Tryptophan only 'Tyr' is acceptable, not 'Y'

    # since we have already got the v_type, set to position 2 after the period
    i = 2
    
    # --- Position/ ---
    # ignore the '[' or '('
    if variant_string[i] == '[' or variant_string[i] == '(':
        i += 1
        allele = True
    # if '?' unknown or '=' no change expected
    if variant_string[i] == '?' or variant_string[i] == '=':
        variant.position = variant_string[i]
        i += 1
        variant.operator_value = variant_string[i:]
    else:
        # get the position amino acid
        if (i+3) < len(variant_string):
            # get the first amino acid
            if variant_string[i] == '*':
                first_amino_acid = '*'
            else:            
                first_amino_acid = variant_string[i:i+3]
                if not first_amino_acid.isalpha():
                    #check if first char is alphabet
                    first_amino_acid = variant_string[i]
                    i += 1
                else:
                    i += 3
                
            # assume that it is a position value for now
            variant.position = first_amino_acid

            # get the position of the amino acid, which will be stored
            # in the postion intron for now
            start_position = i
            while i < len(variant_string):
                if check_numeric_value(variant_string[i]):
                    i += 1
                else:
                    break

            # get the position value
            position = variant_string[start_position:i]
            
            # assume that it is a position intron value for now
            variant.position_intron = position  
            
            if len(variant_string) > i:
                if variant_string[i] == '_':
                    i += 1
                    if len(variant_string) > i:                    
                        # set the first amino acid to range lower
                        variant.position = ''
                        variant.range_lower = first_amino_acid;
                        # set postion intron value to range lower intron
                        variant.position_intron = ''
                        variant.range_lower_intron = position

                        # get the range upper or second amino acid value
                        if variant_string[i] == '*':
                            variant.range_upper = '*'
                        else:
                            if variant_string[i:i+3].isalpha():                            
                                variant.range_upper = variant_string[i:i+3]
                                i += 3
                            else:
                                varaint.range_upper = variant_string[i]
                                i += 1

                        # get the range upper intron
                        start_position = i
                        while i < len(variant_string):
                            if check_numeric_value(variant_string[i]):
                                i += 1
                            else:
                                break

                        variant.range_upper_intron = variant_string[start_position:i]
                
                # get the operator - the amino acid that has changed
                operator = variant_string[i:len(variant_string)]
                operator_value = ''
                
                if operator[0] == '*':
                    operator = '*'
                elif 'delins' in  operator.lower():
                    operator = 'delins'
                    operator_value = variant_string[i+6:len(variant_string)]
                elif variant_string[i] == '(':
                    operator = variant_string[i:len(variant_string)]
                    operator_value = ''
                elif operator.lower() in ('fs*', 'fsx', 'fster'):
                    f = operator.index('fs*')                    
                    operator_value = operator[f:]
                    operator = operator[0:f]
                else:
                    if variant_string[i:i+3].isalpha():                    
                        operator = variant_string[i:i+3]
                        operator_value = variant_string[i+3:len(variant_string)]
                    else:
                        operator = variant_string[i]
                        operator_value = variant_string[i+1:len(variant_string)]
                
                # set the operator
                variant.operator = operator
                variant.operator_value = operator_value

    return variant
