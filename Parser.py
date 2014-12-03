from Util import Parser_Genomic_cDNA
from Util import Parser_mRNA
from Util import Parser_Protein
from Util.Variant import VariantName

'''
 This is use to parse HGVS nomenclature string and returns a
 variant object with all the values extracted out.
 NB: The VariantID is optional it is only really needed for using
 the solr indexing process.
'''

class Parser:
    @classmethod
    def parse(cls, variantID, variant_string):
        # create a new variant object to store variant info
        variant = VariantName()
        
        # set the orginal variant nomenclature
        variant.variant = variant_string
        
        # sets the variant ID, this is for ingesting data for solr indexing
        variant.ID = variantID
        
        if variant_string[1] == '.':
            # get the variant type
            variant.v_type = variant_string[0].lower()
        
            # cDNA or Genomic
            if variant.v_type == 'c' or variant.v_type == 'g':
                return Parser_Genomic_cDNA.parser(variant_string, variant)

            # Protein
            elif variant.v_type == 'p':
                return Parser_Protein.parser(variant_string, variant)

             # mRNA
            elif variant.v_type == 'm':
                return Parser_mRNA.parser(variant_string, variant)
        
        else:
            # contains just the genomic position or has either NC sequence or chromosome
            # eg: 12341234, chr.17:12341234 or NC_000017.10:12341234
            # is variant_string just a numeric genomic position
            if variant_string.isdigit():
                variant.position = variant_string
            else:
                # nope, "should" have genomic ref in front then or contains an operator at the end
                # check for semicolon
                str_pos = ''
                if ':' in variant_string:
                    str_list = variant_string.split(':')
                    # get the genomic ref
                    if 'chr' in str_list[0].lower() or 'nc_' in str_list[0].lower():
                        variant.genomic_ref = str_list[0]
                        str_pos = str_list[1]
                else:
                    str_pos = variant_string
                
                if str_pos.isdigit():
                    # if str_pos is only numeric then it only contains the position
                    variant.position = str_pos
                else:
                    i = 0
                    while i < len(str_pos):    
                        # position and operator detected after alpha char
                        if str_pos[i].isalpha():
                            variant.position = str_pos[0:i]
                            variant.operator = str_pos[i:len(str_pos)]
                            break
                        else:
                            i += 1
            
            return variant
                

'''
 This is used for simple quick test by running the Parser along with a variant argument
 it will return you a result of the broken down values of the variant.
'''

def main():
    # optparse import is moved here so it doesn't conflict with IronPython
    from optparse import OptionParser
    optParser = OptionParser()
    optParser.add_option("-v", "--variant", dest="variant",
                         help="Enter variant to test eg: 'c.123g>t' NB: its best to include the quotes")

    options, args = optParser.parse_args()
    
    parser = Parser()
    variant = parser.parse("", options.variant) # for testing the id is left blank
    
    if variant.ID == "":
        print "ID: -"
    else:
        print "ID: " + variant.ID
    
    if variant.genomic_ref == "":
        print "genomic_ref: -"
    else:
        print "genomic_ref: " + variant.genomic_ref
    
    if variant.v_type == "":
        print "v_type: -"
    else: 
        print "v_type: " + variant.v_type

    if str(variant.position) == "":
        print "position: -"
    else: 
        print "position: " + str(variant.position)

    if str(variant.position_intron) == "":
        print "position_intron: -"
    else: 
        print "position_intron: " + str(variant.position_intron)

    if str(variant.range_lower) == "":
        print "range_lower: -"
    else: 
        print "ranger_lower: " + str(variant.range_lower)

    if str(variant.range_lower_intron) == "":
        print "range_lower_intron: -"
    else: 
        print "range_lower_intron: " + str(variant.range_lower_intron)

    if str(variant.range_upper) == "":
        print "range_upper: -"
    else: 
        print "range_upper: " + str(variant.range_upper)

    if str(variant.range_upper_intron) == "":
        print "range_upper_intron: -"
    else: 
        print "range_upper_intron: " + str(variant.range_upper_intron)

    if variant.operator == "":
        print "operator: -"
    else: 
        print "operator: " + variant.operator

    if variant.operator_value == "":
        print "operator_value: -"
    else:
        print "operator_value: " + variant.operator_value

    if variant.allele == "":
        print "allele: -"
    else:
        print "allele: " + variant.allele
        
    print "Original Value: " + variant.ToString()
    

    
if __name__ == "__main__":
    main()
    
