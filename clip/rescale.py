    
def scale_serpent_to_origen(serpent_volume):
    """
    Function for performing the volume conversion to make Serpent results comparable to ORIGEN ones.
    ORIGEN scales the results to 1 ton of U, so the serpent volume must be scaled to match.
    """
    
    fuel_density = 10.41 #10.41 g/cm^3 as default
    fuel_uranium_density = fuel_density * 0.88 #default 88% of the mass is U in UO2
    standard_volume = 1000000/fuel_uranium_density #ORIGEN results are often normalized to 1 ton of U, Serpent material results are conventration per cm^3
    #serpent_volume = 0.508958   #My example data has a pin radius of 0.41 which means a pin cell volume of pi * 0.41^2 * 1 = 0.508 cm^3.

    scale = standard_volume / serpent_volume
    return scale