from Util import Validate_Genomic_cDNA
from Util import Validate_mRNA
from Util import Validate_Protein
from Util import ValidValues
from Parser import Parser

class Validator:
    @classmethod
    def validate(cls, variant_string):
        # get the variant breakdown from the parser     
        parser = Parser()
        variant = parser.parse('', variant_string) # for validation we can leave ID(the 1st param) blank
        
        # If parsing failed - ie: no values where properly indexed
        if variant == None:
            return False
        
        # Genomic and cDNA - possibilities: c.112g>t, g.12345678, 12345678, NC_000017.10:12345678 or Chr.17:12345678
        if (variant_string[0].lower() == 'g' or variant_string[0].lower() == 'c' or variant_string[0].lower() == 'n'
            or variant_string[0].isdigit()):
            return Validate_Genomic_cDNA.validate(variant)

        # mRNA
        elif variant_string[0].lower() == 'm':
            return Validate_mRNA.validate(variant)

        # Protein
        elif variant_string[0].lower() == 'p':
            return Validate_Protein.validate(variant)
        
        # if nothing else, then fail
        else:
            return False

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
    
    print Validator.validate(options.variant)


if __name__ == "__main__":
    main()

