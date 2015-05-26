class VariantName:
    ID = '' # variant id used for data ingesting in solr
    v_type = ''
    genomic_ref = ''
    position = '' #used for cdna and genomic positioning
    position_intron = ''
    range_lower = '' 
    range_lower_intron = ''
    range_upper = ''
    range_upper_intron = ''
    operator = ''
    operator_value = ''
    allele = ''
    # used to display short sequence repeat and substitution when
    # there is no operator symbol to defined the display of the type
    change_type = '' 
    #change_value = '' 
    
    # the original variant nomenclature
    def ToString(self):
        if self.v_type:
            if self.position:
                return (self.v_type + "." + self.InsertAlleleToPosition(self.position) + self.position_intron + 
                        self.operator + self.operator_value)
            else:    
                return (self.v_type + "." + self.InsertAlleleToPosition(self.range_lower) + self.range_lower_intron +
                        "_" + self.range_upper + self.range_upper_intron + 
                        self.operator + self.operator_value)
                        
        if self.genomic_ref:
            return self.genomic_ref + ":" + self.position + self.operator + self.operator_value
        else:
            return self.position + self.operator + self.operator_value
            
    # appends the missing '[' back to the position        
    def InsertAlleleToPosition(self, position):
        if self.allele:
            if self.allele == 'Mosaicism':
                position = '=/' + position
            elif self.allele == 'Chimerism':
                position = '=//' + position
            else:
                position = '[' + position
        
        return position
            