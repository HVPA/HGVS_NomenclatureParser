from Util import check_value
from Util import check_intron_value
from Util import check_numeric_value
from Util import get_repeater_value
from Variant import VariantName
import ValidValues

def validate(variant):
    # check each values of variant
    # genomic_ref
    if variant.genomic_ref.strip() != '':
        # check if starting with chr or nc_
        if 'chr' in variant.genomic_ref.lower():
            # check for numeric values after 'chr'
            if not variant.genomic_ref[3:].isdigit():
                return False
        
        elif 'nc_' in variant.genomic_ref.lower():
            # check for numeric values after 'nc_'
            try:
                float(variant.genomic_ref[3:])
            except:
                return False
        else:
            return False
    
    # position
    if variant.position.strip() != '':
        # simple check if position is numeric
        if not check_value(variant.position):
            return False
        
    # position_intron
    if variant.position_intron.strip() != '':
        # if position_intron has a value then position must have a value too.
        if variant.position != '':
            if not check_intron_value(variant.position_intron):
                return False
        else:
            return False
    
    # range_lower
    if variant.range_lower.strip() != '':
        # if there is a value in the range_lower then position must be empty
        if variant.position.strip() == '':
            if not check_value(variant.range_lower):
                return False
        else:
            return False
    
    # range_lower_intron
    if variant.range_lower_intron.strip() != '':
        # if range_lower_intron has a value then range_lower must have a value too.
        if variant.range_lower.strip() != '':
            if not check_intron_value(variant.range_lower_intron):
                return False
        else:
            return False

    # range_upper
    if variant.range_upper.strip() != '':
    # if range_upper has a value then range_lower must have a value to
        if variant.range_lower.strip() != '':
            if not check_value(variant.range_upper):
                return False
        else:
            return False
    
    # range_upper_intron
    if variant.range_upper_intron.strip() != '':
        # if range_upper_intron has a value then range_upper must hava a value too
        if variant.range_upper.strip() != '':
            if not check_intron_value(variant.range_upper_intron.strip()):
                return False
        else:
            return False

    operator_is_repeat = False
    # operator
    if variant.operator.strip() != '':
        if variant.operator not in ValidValues.operators:
            # if operator contains a '>'
            if '>' in variant.operator:
                # check if operator is a sub
                if (variant.operator[0].lower() not in ValidValues.nucleotides):
                    return False
                if (variant.operator[1] != '>'):
                    return False
                if (variant.operator[2].lower() not in ValidValues.nucleotides):
                    return False
            else:
                # contains only nucleotides for repeat
                if variant.operator[0].lower() in ValidValues.nucleotides:
                    i = 1 # check the 1st value move to next one
                    operator_is_repeat = True
                    while i < len(variant.operator):
                        if variant.operator[i].lower() in ValidValues.nucleotides:
                            i += 1
                        else:
                            return False
                else:        
                    # get the repeater range value
                    if not get_repeater_value(variant.operator):
                        return False

    # operator value
    if operator_is_repeat: # if operator is a repeat then we check the repeat range
        if variant.operator_value:
            if not get_repeater_value(variant.operator_value):
                return False
        
    # if it survived the checks then return true
    return True

