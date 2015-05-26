from Variant import VariantName
from Util import get_value
from Util import get_operator

def parser(variant_string, variant): 
    # since we have already got the v_type, set to position 2 after the period
    i = 2
