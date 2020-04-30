
#Conversion between ORIGEN isotope name format (e.g Cs137) and Serpent bumat format (e.g 55137)
isotope_name_list_ORIGEN = ["Ce144","Cs134","Cs137","Eu154","Ru106","Sr90"]
isotope_name_list_Serpent = ["58144","55134","55137","63154","44106","38090"]

#isotope masses in u
isotope_mass_list = [143.913647, 133.906718, 136.907090, 153.922979, 105.907330, 89.907738]

def convert_isotope_name(isotope_name, to_this_format):
    """
    Function for converting an isotope name in ORIGEN format to Serpent or vice versa.
    ORIGEN uses the format \"Cs137\" while Serpent uses the format \"55137\"
    """
    
    if to_this_format == "ORIGEN":
        if isotope_name in isotope_name_list_Serpent:
            return isotope_name_list_ORIGEN[isotope_name_list_Serpent.index(isotope_name)]
        else:
            return ""
    elif to_this_format == "Serpent":
        if isotope_name in isotope_name_list_ORIGEN:
            return isotope_name_list_Serpent[isotope_name_list_ORIGEN.index(isotope_name)]
        else:
            return ""
    else:
        print("convert_isotope_name called with unsupported format, should be ORIGEN or Serpent")
        return ""
    
def get_isotope_mass(isotope_name, name_format):
    """
    Function for getting the mass of selected nuclides. 
    This is needed when converting a Serpent material file, given in atoms/cm^3, to a mass in g/cm^3
    """
    if name_format == "Serpent":
        if isotope_name in isotope_name_list_Serpent:
            return isotope_mass_list[isotope_name_list_Serpent.index(isotope_name)]
        else:
            return 0
    elif name_format == "ORIGEN":
        if isotope_name in isotope_name_list_ORIGEN:
            return isotope_mass_list[isotope_name_list_ORIGEN.index(isotope_name)]
        else:
            return 0
    else:
        print("get_isotope_mass called with unsupported format, should be ORIGEN or Serpent")
        return 0
    