import re
import math

from clip.isotope_data import convert_isotope_name
from clip.isotope_data import get_isotope_mass

avogadros_number = 6.022141*(10**23) #For converting atomic densities to mass densities

def convert_to_ORIGEN_binning(spectrum_energies, spectrum_counts, bin_edges):
    """
    Function for converting a gamma emisison spectrum to an ORIGEN-binned one.
    """
    
    #note that ORIGEN splits a gamma peak in two bins if it is close to the bin boundary, 
    #and adjustst the count for each bin to preserve total energy rather than total count.
    
    number_of_bins = len(bin_edges) - 1
    bin_counts = [0] * number_of_bins
    
    for i in range(0,len(spectrum_energies)):
        energy = spectrum_energies[i]
        counts = spectrum_counts[i]

        #Check that the energy is within the binned region.
        if energy > bin_edges[0] and energy < bin_edges[number_of_bins]:
            
            #get the right bin
            for bin in range(0,number_of_bins):
                if bin_edges[bin] <= energy and energy < bin_edges[bin+1]:
                    
                    bin_mid_energy = (bin_edges[bin] + bin_edges[bin+1])/2
                    
                    f = (energy - bin_edges[bin])/(bin_edges[bin+1] - bin_edges[bin])
                    
                    if f < 0.03 and bin > 0:
                        #Close to a bin edge and a lower bin exists, so split the counts evenly between the two.
                        #Follows the procedure outlined in the ORIGEN documentation
                        bin_counts[bin] += counts * (energy/bin_mid_energy) / 2
                        
                        lower_bin_mid_energy = (bin_edges[bin-1] + bin_edges[bin])/2
                        
                        bin_counts[bin - 1] += counts * (energy/lower_bin_mid_energy) / 2
                        
                    elif f > 0.97 and bin < number_of_bins - 1:
                        #Close to a bin edge and a higher bin exists, wo split evenly between the bins.
                        bin_counts[bin] += counts * (energy/bin_mid_energy) / 2
                        
                        higher_bin_mid_energy = (bin_edges[bin+1] + bin_edges[bin+2])/2
                        
                        bin_counts[bin + 1] += counts * (energy/higher_bin_mid_energy) / 2
                    else:
                        #All counts in the bin
                        bin_counts[bin] += counts * (energy/bin_mid_energy)
        
    return bin_counts
        

def read_serpent_gamma_spectrum(output_filename):
    """
    Read a Serpent gamma source file, and return a spectrum that can be used by the prediction functions. 
    """
    
    f = open(output_filename, 'r')
    Serpent = f.read()
    
    if len(Serpent) < 1:
        print("Failed to read Serpent gamma spectrum file " + output_filename)
        return [],[]
    
    spectrum_energies = []
    spectrum_counts = []
    
    #Gamma line data are 7 values per line, separated by spaces.
    spectrum_pattern = re.compile("([0-9]+)\s+([0-9.E+-]+)\s+([0-9.E+-]+)\s+([0-9.E+-]+)\s+([0-9.E+-]+)\s+([0-9.E+-]+)\s+([0-9.E+-]+)\s*")
    
    spectrum_list = re.findall(spectrum_pattern, Serpent)
    
    #Add each emission line ot the total spectrum.
    for isotope in spectrum_list:
        
        #Obtain needed data. there are 7 data columns in total.
        photons_per_decay = float(isotope[1])   #specific intensity (photons per decay)
        total_activity = float(isotope[2])      #Total emission rate  (photons/sec)
        gamma_energy = float(isotope[4])        #Emission line energy
        relative_intensity = float(isotope[5])  #relative intensity (photons per decay)
        
        spectrum_energies.append(gamma_energy)
        spectrum_counts.append(total_activity / photons_per_decay * relative_intensity)
        
    return spectrum_energies, spectrum_counts
    
def read_serpent_isotope_contents(output_filename, isotope_list):
    """
    #Read a Serpent bumat file, and return the contents of the selected isotopes. 
    """
    
    f = open(output_filename, 'r')
    Serpent = f.read()
    
    if len(Serpent) < 1:
        print("Failed to read Serpent gamma spectrum file " + output_filename)
        return [],[]
    
    isotope_contents = [0.0] * len(isotope_list)
    
    header_pattern = re.compile("mat\s*([A-Za-z0-9]+)\s*([0-9.E-]+)\s*vol\s*([0-9.E-]+)")
    
    if re.search(header_pattern, Serpent):
        header = re.search(header_pattern, Serpent)
    else:
        print("Failed to find Serpent header data")
        return []
    
    material_volume = float(header[3]) #THis is the surface area of the circular cross-section of the fuel rod, but the height is 1cm so it is also the volume in cm^3
    
    material_pattern = re.compile("\s*([0-9]+).09c\s*([0-9.E+-]+)")
    
    material_list = re.findall(material_pattern, Serpent)
    
    for material in material_list:
        material_ZAI = material[0]
        material_concentration = float(material[1])
        
        isotope_name = convert_isotope_name(material_ZAI, "ORIGEN")
        
        if isotope_name in isotope_list:
            #convert the concentration to a mass per ton fuel
            isotope_mass = get_isotope_mass(material_ZAI, "Serpent")
            
            temp = material_concentration * 10**24    #convert from atoms per cm^3 in barn to atoms/cm^3
            isotope_weight = temp * isotope_mass / avogadros_number #Convert to grams of the isotope per cm^3

            isotope_contents[isotope_list.index(isotope_name)] = isotope_weight
        
    return isotope_contents
     
