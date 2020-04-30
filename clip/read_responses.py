import re
import math

def read_binned_response(response_filename):
    """
    Function for reading a binned response, returning the bin structure, contents and uncertainty
    """
    f = open(response_filename, 'r')
    text = f.read()
    textlines = text.splitlines()
    
    if len(textlines) < 2:
        print("Failed to read binned response file " + response_filename)
        return [0], [0], [0]
    
    bin_count = [0] * (len(textlines)-1)
    bin_edges = [0] * (len(textlines))
    bin_uncertainty = [0] * (len(textlines)-1)
    
    #First line is a header, all subsequent lines are data.
    for i in range(1,len(textlines)):
        #In case the source uses decimal comma.
        split_line = textlines[i].replace(",",".")
        
        #tab-separated table
        split_line = split_line.split("\t")
        
        if len(split_line) < 4:
            print("Malformed line in response file " + response_filename)
            print("The data should be in four columns")
            print("The line was:")
            print(textlines[i])
            return [0], [0], [0]
        
        #Put the data in arrays
        bin_edges[i-1] = float(split_line[0])
        bin_count[i-1] = float(split_line[2])
        bin_uncertainty[i-1] = float(split_line[3])
        
    #Final upper bin edge.
    bin_edges[len(textlines)-1] = float(split_line[1])
    
    return bin_edges, bin_count, bin_uncertainty

def read_sampled_response(response_filename):
    """
    Function for reading a sampled response, returning the sampled energies, the response per energy and the uncertainty in the response.
    """
   
    f = open(response_filename, 'r')
    text = f.read()
    textlines = text.splitlines()
    
    if len(textlines) < 2:
        print("Failed to read sampled response file " + response_filename)
    
    response = [0] * (len(textlines)-1)
    sampled_energies = [0] * (len(textlines)-1)
    uncertainty = [0] * (len(textlines)-1)
    
    #First line is a header, all subsequent lines are data.
    for i in range(1,len(textlines)):
        #In case the source uses decimal comma.
        split_line = textlines[i].replace(",",".")
        
        #tab-separated table
        split_line = split_line.split("\t")
        
        if len(split_line) < 3:
            print("Malformed line in response file " + response_filename)
            print("The data should be in three columns.")
            print("The line was:")
            print(textlines[i])
            return [0], [0], [0]
        
        #Put the data in arrays
        sampled_energies[i-1] = float(split_line[0])
        response[i-1] = float(split_line[1])
        uncertainty[i-1] = float(split_line[2])
    
    return sampled_energies, response, uncertainty

def read_isotope_response(response_filename, response_type):
    """
    Function for reading an isotope response, for a respone type of \"decay\" or \"mass\"
    depending on whether the isotopes are given as an activity or in weight.
    """

    f = open(response_filename, 'r')
    text = f.read()
    textlines = text.splitlines()
    
    isotope_list = [] 
    isotope_response_activity = []
    isotope_uncertainty_activity = []
    isotope_response_mass = [] 
    isotope_uncertainty_mass = []
    
    #first line is a header, all remaining lines are data
    for i in range(1,len(textlines)):
        
        #Just to make sure a final newline does not cause any problems
        if len(textlines[i]) > 5:
            line = textlines[i].split("\t")
            isotope_list.append(line[0])
            isotope_response_activity.append(float(line[1]))
            isotope_uncertainty_activity.append(float(line[2]))
            isotope_response_mass.append(float(line[3]))
            isotope_uncertainty_mass.append(float(line[4]))
        
    if response_type == "decay":
        return isotope_list, isotope_response_activity, isotope_uncertainty_activity
    elif response_type == "mass":
        return isotope_list, isotope_response_mass, isotope_uncertainty_mass
    else:
        print("Read_isotope_response called with the response type not being \"decay\" or \"mass\", it was " + response_type)
        return [0], [0], [0]
        
