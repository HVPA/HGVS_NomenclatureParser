from Variant import VariantName
from Util import get_value
from Util import get_operator
from ValidValues import operators, nucleotides

def parser(variant_string, variant): 
    # since we have already got the v_type, set to position 2 after the period
    i = 2
    
    # --- Position/ ---
    # get the position
    position_list = get_value(i, variant_string)
    
    variant.position = position_list[0] # get the position value
    i = position_list[1] # get the position index
    allele = position_list[2] # if variant has variation in allele
    
    # get the position intron
    if i < len(variant_string): # if the index is still within the variant_string index range
        if variant_string[i] == '-' or variant_string[i] == '+':
            position_intron_list = get_value(i, variant_string)
            if position_intron_list[0] == '?':
                variant.position_intron = '?'
            else:
                try:
                    variant.position_intron = position_intron_list[0]
                except:
                    variant.position_intron = ''
            # increment the counter
            i = position_intron_list[1]
            
    # --- /Position ---    

    #get the range position will increment if '_' is detected
    if i < len(variant_string):
        if variant_string[i] == '_':
            i += 1

            # Since its actually a range variant, use range_lower and clear position variable
            variant.range_lower = variant.position
            variant.position = ''
            variant.range_lower_intron = variant.position_intron
            variant.position_intron = ''

            # --- Higher/ ---
            range_list = get_value(i, variant_string)
            variant.range_upper = range_list[0]
            i = range_list[1]
            
            # get the position intron
            if i < len(variant_string):
                if variant_string[i] == '-' or variant_string[i] == '+':
                    position_intron_list = get_value(i, variant_string)
                    if position_intron_list[0] =='?':
                        variant.range_upper_intron = '?'
                    else:
                        try:
                            variant.range_upper_intron = position_intron_list[0]
                        except:
                            variant.range_upper_intron = ''
                    # increment the counter
                    i = position_intron_list[1]

    #get the substitution formula
    if i < len(variant_string):
        #variant.operator = get_operator(i, variant_string)
        # gets the last remain chars from the string it should contain a operator
        raw_operator = variant_string[i:len(variant_string)]
        
        # if operator is a sub
        if '>' in raw_operator:
            variant.operator = variant_string[i:i+3]
            # if there is anything left at the end of the sub operator then
            # it will become the operator value.
            if i < len(variant_string):
                variant.operator_value = variant_string[i+3:len(variant_string)]
        else:
            # search for other operator from the 
            found_operator = ''
            for op in operators:
                if op in raw_operator.lower():
                    found_operator = op
                    break

            variant.operator = found_operator

            # get operator value for delins
            if found_operator == 'delins':
                variant.operator_value = variant_string[i+6:len(variant_string)]

            # gets the nucleotide that has been inverted, deleted or duplicated from
            # the specified position/s we collect the nucleotide or position value from
            # the operator value.
            if found_operator in ['inv', 'del', 'dup', 'ins']:
                variant.operator_value = variant_string[i+3:len(variant_string)]

            # check if operator is variability of short repeats
            if found_operator.strip() == '':
                start_operator = i
                while i < len(variant_string):
                    if variant_string[i].lower() in nucleotides:
                        i += 1
                    else:
                        break
                # this only contains the repeat
                variant.operator = variant_string[start_operator:i]                
                # the end will be the range of the repeat only if variant.operator contains a value
                if variant.operator.strip() != '':
                    variant.operator_value = variant_string[i:len(variant_string)]
                # TODO: the operator value above will be in a range (eg:7-9) this should be
                # broken down so it can be indexed and searched based on the range value
                
                # this should skip the below process if an operator was found
                found_operator = variant.operator
            
            # if no operator found then we just dump what ever is at the end this should
            # allow the validator to validate the operator as invalid.
            # It is highly possible the end is the repeat range without a nucleotide (eg:c.12_45(5-9))
            if found_operator.strip() == '':
                variant.operator = variant_string[i:len(variant_string)]
            
            # TODO: Above needs "short repeat", gene converation, translocation -- Alan 13/11/2010
            
        # get the allele type
        if allele:
            # Changes in diff alleles
            # Mosaicism
            if allele == 'Mosaicism':
                variant.allele = allele
        
            # Chimerism
            if allele == 'Chimerism':
                variant.allele = allele
                
            if variant.operator_value != '':
                if variant.operator_value[0] == ';':
                    variant.allele = 'Changes in different alleles'
            
                # Two variations in one allele
                elif '(;)' in variant.operator_value:
                    variant.allele = 'Two variations in one allele'
            
                # Two sequence changes
                elif '];[' in variant.operator_value:
                    variant.allele = 'Two sequence changes with alleles unknown'
    
    return variant

