
from scipy.interpolate import interp1d
from scipy.integrate import quad

def get_binned_response_function(energies, response, bin_edges):
    """
    Function for binning a response function, to convert a sampled response to a binned one. 
    """
    
    #The simulations are done for various initial gamma energies (the variable energies)
    #and provide the average number of vertically directed Cherenkov photons produced
    # per decay (the variable response). This is, in effect, a sampling of the response function we are after. 
    #What we want to do is to convert this response funciton to a binned format, 
    #matching the binned gamma spectrum provided by ORIGEN.
    # As a result, we will for each bin know the average response for each decay with energy 
    # within a bin. 
    
    #This procedure follows the rebinning procedure explained in 
    #Knoll, chapter 18.IV.B, "Spectrum alignment".
    #Hence, we interpolate the sampled response function, numerically integrate
    # the area between any two bin edges, and let that area divided by the width be
    # the average response for the bin. 
    
    func = interp1d(energies, response, kind='cubic')
    bin_response = [0] * (len(bin_edges) - 1)
    
    min_energy = energies[0]
    max_energy = energies[len(energies)-1]
    
    for i in range(0, len(bin_edges)-1):
        if bin_edges[i] < min_energy:
            #Have not sampled this low, so cannot interpolate
            bin_response[i] = 0
        elif bin_edges[i] > min_energy and bin_edges[i+1] < min_energy:
            #The bin covers some low energies not sampled.
            integral = quad(func, min_energy, bin_edges[i+1])
            bin_response[i] = integral[0] / (bin_edges[i+1] - min_energy)
        elif bin_edges[i] >= min_energy and bin_edges[i+1] <= max_energy:
            #have sampled the response function for this energy
            integral = quad(func, bin_edges[i], bin_edges[i+1])
            bin_response[i] = integral[0] / (bin_edges[i+1] - bin_edges[i])
        elif bin_edges[i] < max_energy and bin_edges[i+1] > max_energy:
            #The bin covers some high energies not sampled
            integral = quad(func, bin_edges[i], max_energy)
            bin_response[i] = integral[0] / (max_energy - bin_edges[i])
        elif bin_edges[i+1] > max_energy:
            #Have not sampled this high, so cannot interpolate
            bin_response[i] = 0

    return bin_response