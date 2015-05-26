
"""
 Gets the intron value from the position of the index in the variant string.
"""
def get_value(index, variant_string):
    value = ''
    start_index = index
    allele = None
    while index <= len(variant_string):
        try:
            skip = False
            #check if it starts with a negative 
            if index == start_index:
                if variant_string[index] == '[':
                    skip = True
                    # Mosaicism
                    if '=/' in variant_string:
                        start_index += 3
                        index += 3
                        allele = 'Mosaicism'
                    # Chimerism
                    elif '=//' in variant_string:
                        start_index += 4
                        index += 4
                        allele = 'Chimerism'
                    else:
                        start_index += 1
                        index += 1
                        allele = True
                    
                if (variant_string[index] == '-' or variant_string[index] == '*' or 
                    variant_string[index] == '+'):
                    index += 1
                    skip = True

            if not skip:
                if variant_string[index] == '?':
                    value = '?'
                    index += 1
                    break
                else:            
                    if variant_string[index] == '*':
                        value = variant_string[start_index:index]
                        if index+1 < len(variant_string):
                            break
                    elif not variant_string[index].isdigit():
                        value = variant_string[start_index:index]
                        break
                index += 1
        except IndexError:
            # the variant string entered is not complete and has eruptly ended so 
            # now we have caught an index out of rangei exception. 
            # get the last known value
            value = variant_string[start_index:index]
            break
            
    return [value, index, allele]

"""
 Gets the 3 digit operator from the position of the index in the variant string.
 Assumption: removed the validation of the operator here and assuming that the
 the operator will only be 3 char long. Validation should be handled by the client.
"""
def get_operator(index, variant_string):
    operator = ''
    if variant_string[index].isalpha():
        # operator should be 3 char long, if any longer it will be cut off
        # if shorter than it will throw out of range except in that case
        # we try to get the operator with what ever we have.
        try:
            operator = variant_string[index:index+3]
        except:
            operator = variant_string[index:]
        
    return operator


"""
 Checks if a string of text is a numeric value by converting it to a float value
 if successful it returns true, if it throws an exception it returns false.
"""
def check_numeric_value(numeric_string):
    # Allows '*' to be in front of numeric value or '*' on its own. e.g: c.*g>t or c.*123g>t
    # When '*' is on its own it is considered a wildcard search in the HVP portal
    if numeric_string == '-*' or numeric_string == '+*':
        return True
    
    if numeric_string[0] == '*':
        if numeric_string[1:].isdigit():
            return True
        else:
            return False
    else:
        try:
            float(numeric_string)
            return True
        except:
            return False
        
        
"""
 Check the value ranges are valid. Used by Validator classes
"""
def check_value(value):
    if not check_intron_value(value):
        return False

    # if it survived all the checks up to here, then its valid
    return True


"""
 Check the intron value ranges are valid. Used by Validator classes
"""
def check_intron_value(value):
    if value[0] == '-' or value[0] == '+':
        if not check_numeric_value(value):
            return False
    # if position first char is '?' then it should be the only char
    elif value[0] == '?':
        if len(value) != 1:
            return False
    # if it survived all the checks up to here, then its valid
    return True

"""
 Check the repeating ranges value
"""
def get_repeater_value(value):
    if value[0] == '(':
        i = 1
        underscore = False
        while i < len(value):
            if check_numeric_value(value[i]):
                i += 1
            elif not underscore and value[i] == '_':
                # there should be only one underscore
                i += 1
                underscore = True
            elif (i + 1) == len(value) and value[i] == ')':
                # this is the last char in string must be ')'
                return True
            else:
                return False
    elif value[0] == '[':
        #import pdb
        #pdb.set_trace()
        i = 1
        while i < len(value):
            if check_numeric_value(value[i]):
                i += 1
            else:
                if value[i] == ']':
                    # if there is more after the 1st allele
                    if (i + 1) != len(value):
                        i += 1
                        if value[i] == '+':
                            i += 1
                            if (i + 1) != len(value):
                                if value[i] == '[':
                                    i += 1
                                    while i < len(value):
                                        if check_numeric_value(value[i]):
                                            i += 1
                                        elif (i + 1) == len(value) and value[i] == ']':
                                            return True
                                        else:
                                            return False
                                else:
                                    return False
                            else:
                                return False
                        else:
                            return False
                    else:
                        return True
    else:
        return False # if it doesn't begin with '(' or '[' then False

"""
 Splits a string into an array list where each item char size will be based on
 the specified size. eg: split('abcdefghi', 3) == ['abc','def','ghi']
"""
def split(input, size):
    return [input[start:start+size] for start in range(0, len(input), size)]
