import math
from scipy.interpolate import interp1d

from clip.read_ORIGEN_output import *
from clip.read_responses import *
from clip.setup_response_function import *
from clip.read_serpent_output import *
from clip.isotope_data import *
from clip.rescale import *

Binned_gamma_response_folder = "Data/Binned_gamma_response/"
Binned_beta_response_folder = "Data/Binned_beta_response/"
Sampled_gamma_response_folder = "Data/Sampled_gamma_response/"
Sampled_beta_response_folder = "Data/Sampled_beta_response/"
Isotope_gamma_response_folder = "Data/Isotope_gamma_response/"
Isotope_beta_response_folder = "Data/Isotope_beta_response/"

def Predict_binned_response(spectrum, spectrum_uncertainties, response, response_uncertainties):
    """This function makes a Cherenkov light intensity prediction based on a binned response function



    Parameters

    ----------

    spectrum : array of floats

        Per-bin gamma-ray emission intensities.

    spectrum_uncertainties : array of floats

        Uncertainties in the per-bin gamma-ray emission intensities.
        
    response : array of floats

        Per-bin gamma-ray Cherenkov light response.
        
    response_uncertainties : array of floats

        Uncertanties in the per-bin gamma-ray Chherenkov light response.


    Returns

    -------

    two float values

        the Cherenkov light intensity prediction and the uncertainty in the prediction

    """
    
    prediction = 0.0
    uncertainty = 0.0
    
    for i in range (0,len(spectrum)):
        #Per bin response
        prediction += spectrum[i] * response[i]
        
        uncertainty_sum = 0
        
        #Check that the spectrum or the response has counts, otherwise let the 
        #prediction be 0 and the uncertainty too.
        if spectrum[i] > 0:
            uncertainty_sum += (spectrum[i]*response[i])**2 * (spectrum_uncertainties[i]/spectrum[i])**2
            
        if response[i] > 0:
            uncertainty_sum += (spectrum[i]*response[i])**2 * (response_uncertainties[i]/response[i])**2
        
        #Sum of square of uncertainty
        uncertainty = uncertainty + uncertainty_sum
    
    #And the square root to obtain a RMSE value.
    uncertainty = math.sqrt(uncertainty)
    
    return prediction, uncertainty

def Predict_sampled_response(spectrum_energies, spectrum_intensities, spectrum_uncertainties, response_energies, response_counts, response_uncertainties):
    """This function makes a Cherenkov light intensity prediction based on a response function sampled at various energies



    Parameters

    ----------

    spectrum_energies : array of floats

        The energy of the discreet gamma lines in the gamma spectrum.
        
    spectrum_intensities : array of floats

        The intensity (photons/second) of the discreet gamma lines in the gamma spectrum.

    spectrum_uncertainties : array of floats

        Uncertainties in the gamma spectrum intensities.
        
    response_energies : array of floats

        The gamma-ray energies that the response function was simulated for.
        
    response_counts : array of floats

        The number of Cherenkov photons produced for a gamma-ray with energy from response_energies.
        
    response_uncertainties : array of floats

        Uncertanties in the response function (i.e. in the response_counts values).


    Returns

    -------

    two float values

        the Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    #interpolate response functions
    response_function = interp1d(response_energies, response_counts, kind='cubic')
    response_uncertainty_function = interp1d(response_energies, response_uncertainties, kind='cubic')
    
    response_min_energy = response_energies[0]
    response_max_energy = response_energies[len(response_energies) - 1]
    
    prediction = 0
    uncertainty_squared = 0
    
    for i in range(0,len(spectrum_energies)):
        if spectrum_energies[i] >= response_min_energy and spectrum_energies[i] < response_max_energy:

            gamma_response = spectrum_intensities[i]*response_function(spectrum_energies[i])
            prediction += gamma_response
                
            #sum of square of the uncertainties
            if spectrum_intensities[i] > 0:
                #Spectrum uncertainty
                uncertainty_squared += (gamma_response)**2 * (spectrum_uncertainties[i]/spectrum_intensities[i])**2
            
            if response_function(spectrum_energies[i]) > 0:
                #Response uncertainty, as interpolated
                uncertainty_squared += (gamma_response)**2 * (response_uncertainty_function(spectrum_energies[i])/response_function(spectrum_energies[i]))**2
            
    uncertainty = math.sqrt(uncertainty_squared)
    
    return prediction, uncertainty

def Predict_ORIGEN_binned_gamma_response(ORIGEN_filename, cooling_time_header, response_filename):
    """This function reads a binned gamma spectrum from the ORIGEN output and a binned response to make a Cherenkov light intensity prediction



    Parameters

    ----------

    ORIGEN_filename : string

        Path and name of the ORIGEN output file.
        
    cooling_time_header : string

        The header in the ORIGEN output colums that the data is to be read from.

    response_filename : string

        Path and name of the binned response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction

    """
    
    prediction = 0
    uncertainty = 0

    #Load data
    spectrum_edges, spectrum_counts = read_ORIGEN_gamma_spectrum(ORIGEN_filename, cooling_time_header) 
    response_edges, response_counts, response_uncertainties = read_binned_response(response_filename)
    
    #Check that data has been loaded
    if len(spectrum_edges) == 1 or len(response_edges) == 1:
        print("Failed in loading data for ORIGEN binned response prediction")
        return 0,0
    
    #Check that bin structure matches.
    if len(spectrum_edges) != len(response_edges):
        print("Different bin structure for the gamma emissions and the simulated response")
        return 0,0
    
    for i in range(0,len(spectrum_edges)):
        if spectrum_edges[i] != response_edges[i]:
            print("Different bin structure for the gamma emissions and the simulated response")
            return 0,0
        
    #Uncertainty in gamma spectrum not provided by ORIGEN, so do not include here.
    spectrum_uncertainties = [0] * len(spectrum_counts)    
    prediction, uncertainty = Predict_binned_response(spectrum_counts, spectrum_uncertainties, response_counts, response_uncertainties)    
        
    return prediction, uncertainty

def Predict_beta_binned_response(spectrum_edges, spectrum_counts, response_filename):
    """This function predicts the Cherenkov light intensity from a binned beta response, 
    and takes a binned beta intensity to make a prediction.
    Note that neither ORIGEN or Serpent provides a beta spectrum, so such values must come from elsewhere.



    Parameters

    ----------

    spectrum_edges : array of floats

        The edges of the binned spectrum.
        
    spectrum_counts : array of floats

        The beta activity of each bin. 

    response_filename : string

        Path and name of the binned response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    prediction = 0
    uncertainty = 0
    
    #Load data
    response_edges, response_counts, response_uncertainties = read_binned_response(response_filename)
    
    #Check that data has been loaded
    if len(spectrum_edges) == 1 or len(response_edges) == 1:
        print("Failed in loading data for ORIGEN binned response prediction")
        return 0,0
    
    #Check that bin structure matches.
    if len(spectrum_edges) != len(response_edges):
        print("Different bin structure for the gamma emissions and the simulated response")
        return 0,0
    
    #Check that all bin edges match.
    for i in range(0,len(spectrum_edges)):
        if spectrum_edges[i] != response_edges[i]:
            print("Different bin structure for the gamma emissions and the simulated response")
            return 0,0
    
    #Check that the number of bins matches the bin edges
    if len(spectrum_counts) != len(spectrum_edges) - 1:
        print("The beta bin contents does not match the bin structure")
        return 0,0
        
    #Uncertainty in spectrum is not provided in ORIGEN format, so do not include here.
    spectrum_uncertainties = [0] * len(spectrum_counts)    
    prediction, uncertainty = Predict_binned_response(spectrum_counts, spectrum_uncertainties, response_counts, response_uncertainties)    
        
    return prediction, uncertainty
    
def Predict_isotope_response(isotope_mass_contents, isotope_mass_uncertainty, response, response_uncertainty):
    """This function makes a Cherenkov light intensity prediction based on 
    the isotopic contents of a fuel assembly and an isotope response.



    Parameters

    ----------

    isotope_mass_contents : array of floats

        The mass contents of the various isotopes.
        
    isotope_mass_uncertainty : array of floats

        The uncertainty in the mass contents of the various isotopes.

    response : array of floats

        The per-isotope Cherenkov light production.
        
    response : array of floats

        The uncertainty in the per-isotope Cherenkov light production.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    prediction = 0.0
    uncertainty = 0.0
    
    for i in range (0,len(isotope_mass_contents)):
        #Per isotope response
        prediction = prediction + isotope_mass_contents[i]*response[i]
        
        uncertainty_sum = 0
        
        #Check that the spectrum or the response has counts, otherwise let the 
        #prediction be 0 and the uncertainty too.
        if isotope_mass_contents[i] > 0:
            uncertainty_sum = uncertainty_sum + (isotope_mass_contents[i]*response[i])**2 * ((isotope_mass_uncertainty[i]/isotope_mass_contents[i])**2)
            
        if response[i] > 0:
            uncertainty_sum = uncertainty_sum + (isotope_mass_contents[i]*response[i])**2 * (response_uncertainty[i]/response[i])**2
        
        #Sum of square of uncertainty
        uncertainty = uncertainty + uncertainty_sum
    
    #And the square root to obtain a RMSE value.
    uncertainty = math.sqrt(uncertainty)
    
    return prediction, uncertainty

def Predict_ORIGEN_beta_contents(ORIGEN_filename, cooling_time_header, response_filename):
    """This function makes a Cherenkov light intensity prediction based on the beta-decaying
    isotope contents read from an ORIGEN output file



    Parameters

    ----------

    ORIGEN_filename : string

        Path and name of the ORIGEN output file.
        
    cooling_time_header : string

        The header in the ORIGEN output colums that the data is to be read from.

    response_filename : string

        Path and name of the beta isotope response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    prediction = 0
    uncertainty = 0
    
    #Read all isotopes for which we have a respone defined
    isotope_list, response, response_uncertainty = read_isotope_response(response_filename, "mass")
    
    #read the isotope_list that we have a response for.
    isotope_mass_contents = read_ORIGEN_isotope_contents(ORIGEN_filename, cooling_time_header, isotope_list)

    #ORIGEN provides no uncertainties on each isotope mass, so neglect this 
    #uncertainty contribution for now.
    isotope_uncertainties = [0] * len(isotope_mass_contents)  
    prediction, uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)

    return prediction, uncertainty

def Predict_ORIGEN_gamma_contents(ORIGEN_filename, cooling_time_header, response_filename):
    """This function makes a Cherenkov light intensity prediction based on the gamma-decaying
    isotope contents read from an ORIGEN output file



    Parameters

    ----------

    ORIGEN_filename : string

        Path and name of the ORIGEN output file.
        
    cooling_time_header : string

        The header in the ORIGEN output colums that the data is to be read from.

    response_filename : string

        Path and name of the gamma isotope response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    prediction = 0
    uncertainty = 0
    
    isotope_list, response, response_uncertainty = read_isotope_response(response_filename, "mass")
    
    #read the isotope_list that we have a response for.
    isotope_mass_contents = read_ORIGEN_isotope_contents(ORIGEN_filename, cooling_time_header, isotope_list)

    #ORIGEN provides no uncertainties on each isotope mass, so neglect this 
    #uncertainty contribution for now.
    isotope_uncertainties = [0] * len(isotope_mass_contents)  
    prediction, uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)

    return prediction, uncertainty

def Predict_ORIGEN_sampled_gamma_response(ORIGEN_filename, cooling_time_header, response_filename):
    """This function makes a Cherenkov light intensity prediction based on the binned gamma spectrum 
    read from an ORIGEN output file and a sampled response function.



    Parameters

    ----------

    ORIGEN_filename : string

        Path and name of the ORIGEN output file.
        
    cooling_time_header : string

        The header in the ORIGEN output colums that the data is to be read from.

    response_filename : string

        Path and name of the isotope response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction

    """
    
    prediction = 0
    uncertainty = 0
    
    #Load data
    spectrum_edges, spectrum_counts = read_ORIGEN_gamma_spectrum(ORIGEN_filename, cooling_time_header) 
    response_energies, response_counts, response_uncertainties = read_sampled_response(response_filename)
    
    #Convert from sampled response to the binning used in the ORIGEN gamma spectrum
    binned_response = get_binned_response_function(response_energies, response_counts, spectrum_edges)
    binned_response_uncertainties = get_binned_response_function(response_energies, response_uncertainties, spectrum_edges)
      
    #Uncertainty in gamma spectrum not provided by ORIGEN, so do not include here.
    spectrum_uncertainties = [0] * len(spectrum_counts)    
    prediction, uncertainty = Predict_binned_response(spectrum_counts, spectrum_uncertainties, binned_response, binned_response_uncertainties)    
        
    return prediction, uncertainty

def Predict_serpent_binned_gamma_response(serpent_filename, response_filename):
    """This function makes a Cherenkov light intensity prediction based on the gamma spectrum 
    read from a Serpent output file and a binned response function.



    Parameters

    ----------

    serpent_filename : string

        Path and name of the serpent output file.
        
    response_filename : string

        Path and name of the isotope response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    prediction = 0
    uncertainty = 0
    
    spectrum_energies, spectrum_counts = read_serpent_gamma_spectrum(serpent_filename)
    response_edges, response_counts, response_uncertainties = read_binned_response(response_filename)
    
    ORIGEN_binned_spectrum = convert_to_ORIGEN_binning(spectrum_energies, spectrum_counts, response_edges)
    
    #Uncertainty in gamma spectrum not provided by serpent, so do not include here.
    ORIGEN_binnned_uncertainties = [0] * len(ORIGEN_binned_spectrum)    
    prediction, uncertainty = Predict_binned_response(ORIGEN_binned_spectrum, ORIGEN_binnned_uncertainties, response_counts, response_uncertainties)    
      
    return prediction, uncertainty
        
def Predict_serpent_sampled_gamma_response(serpent_filename, response_filename):
    """This function makes a Cherenkov light intensity prediction based on the gamma spectrum 
    read from a Serpent output file and a sampled response function.



    Parameters

    ----------

    serpent_filename : string

        Path and name of the serpent output file.
        
    response_filename : string

        Path and name of the isotope response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    prediction = 0
    uncertainty = 0
    
    spectrum_energies, spectrum_counts = read_serpent_gamma_spectrum(serpent_filename)
    response_energies, response_counts, response_uncertainties = read_sampled_response(response_filename)
    
    #Uncertainties not provided by Serpent gamma spectrum output
    spectrum_uncertainties = [0] * len(spectrum_energies)
    
    prediction, uncertainty = Predict_sampled_response(spectrum_energies, spectrum_counts, spectrum_uncertainties, response_energies, response_counts, response_uncertainties)

    return prediction, uncertainty

def Predict_serpent_isotope_response(serpent_filename, response_filename):
    """This function makes a Cherenkov light intensity prediction based on the isotope contents 
    read from a Serpent output file and a isotope response function.



    Parameters

    ----------

    serpent_filename : string

        Path and name of the serpent output file.
        
    response_filename : string

        Path and name of the isotope response function.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction

    """
    prediction = 0
    uncertainty = 0
    
    isotope_list, response, response_uncertainty = read_isotope_response(response_filename, "mass")
    
    #read the isotope_list that we have a response for.
    isotope_mass_contents = read_serpent_isotope_contents(serpent_filename, isotope_list)
    
    #ORIGEN provides no uncertainties on each isotope mass, so neglect this 
    #uncertainty contribution for now.
    isotope_uncertainties = [0] * len(isotope_mass_contents)  
    prediction, uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)

    return prediction, uncertainty

def Predict_serpent(serpent_filename, fuel_type, output_type, gamma_response_type, beta_response_type):
    """This function makes a Cherenkov light intensity prediction based on a serpent output.



    Parameters

    ----------

    serpent_filename : string

        Path and name of the serpent output file
        
    fuel_type : string

        The type of fuel assembly, sich as \"PWR17x17\". This name must match a file in the \"Data\" folder.
        
    output_type: string
    
        The type of serpent output. \"spectrum\" for a gamma spectrum file, and \"isotope\" for a material (.bumat) file.
        
    gamma_response_type: string
    
        The type of gamma response to use. \"binned\" for a binend gamma spectrum response \"sampled\" for a sampled resonse, 
        and \"isotope\" for an isotope response. \"None\" to ignore the gamma contribution.
        
    beta_response_type: string
    
        The type of beta response to use.  \"isotope\" for an isotope response, and \"None\" to ignore the beta contribution.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    gamma_prediction = 0
    gamma_uncertainty = 0
    
    if gamma_response_type != "none":
    #Since gamma data and isotope composition comes from different files, allow for beta-only predictions.
        
        if output_type == "spectrum" and gamma_response_type == "binned":
            gamma_prediction, gamma_uncertainty = Predict_serpent_binned_gamma_response(serpent_filename, Binned_gamma_response_folder + fuel_type + ".txt")
            
        elif output_type == "spectrum" and gamma_response_type == "sampled":
            gamma_prediction, gamma_uncertainty = Predict_serpent_sampled_gamma_response(serpent_filename, Sampled_gamma_response_folder + fuel_type + ".txt")
            
        elif output_type == "isotope" and gamma_response_type == "isotope":
            gamma_prediction, gamma_uncertainty = Predict_serpent_isotope_response(serpent_filename, Isotope_gamma_response_folder + fuel_type + ".txt")
        else:
            print("Predict_serpent called with an unsupported combination of Serpent output type and gamma response type")
            print("Implemented combinations are:")
            print("spectrum and binned")
            print("spectrum and sampled")
            print("isotope and isotope")
            return 0,0
    
    #Serpent output does not give any beta decay spectrum, so only isotope predictions can be done here.
    if beta_response_type != "isotope" and beta_response_type != "none":
        print("Predict_serpent called with an unsupported beta response type. It should be \"isotope\" or \"none\"")
        return 0,0
    
    if beta_response_type == "isotope" and output_type == "spectrum":
        print("Beta contribution was requested, but only Serpent gamma data provided. Beta predictions are ignored.")
        beta_prediction = 0
        beta_uncertainty = 0
    elif beta_response_type == "isotope" and output_type == "isotope":
         beta_prediction, beta_uncertainty = Predict_serpent_isotope_response(serpent_filename, Isotope_beta_response_folder + fuel_type + ".txt")
    elif beta_response_type == "none":
        beta_prediction = 0
        beta_uncertainty = 0
    else:
        print("Failed to include beta contents in prediction, unknown combination of Serpent outptu data and beta response type.")
        beta_prediction = 0
        beta_uncertainty = 0
        
    prediction = gamma_prediction + beta_prediction
    uncertainty = math.sqrt(gamma_uncertainty**2 + beta_uncertainty**2)
        
    return prediction, uncertainty
    
    
def Predict_ORIGEN(ORIGEN_filename, cooling_time_header, fuel_type, gamma_response_type, beta_response_type):
    """This function makes a Cherenkov light intensity prediction based on an ORIGEN output.



    Parameters

    ----------

    ORIGEN_filename : string

        Path and name of the ORIGEN output file
        
    cooling_time_header: string
    
        The header in the ORIGEN output colums that the data is to be read from.
        
    fuel_type : string

        The type of fuel assembly, sich as \"PWR17x17\". This name must match a file in the \"Data\" folder.
        

    gamma_response_type: string
    
        The type of gamma response to use. \"binned\" for a binend gamma spectrum response \"sampled\" for a sampled resonse, 
        and \"isotope\" for an isotope response. \"None\" to ignore the gamma contribution.
        
    beta_response_type: string
    
        The type of beta response to use.  \"isotope\" for an isotope response, and \"None\" to ignore the beta contribution.
        

    Returns

    -------

    two float values

        The Cherenkov light intensity prediction and the uncertainty in the prediction.

    """
    
    gamma_prediction = 0
    gamma_uncertainty = 0
    
    if gamma_response_type != "binned" and gamma_response_type != "isotope" and gamma_response_type != "sampled":
        print("Predict_ORIGEN called with an unsupported gamma response type. It should be \"binned\", \"isotope\" or \"sampled\"")
        return 0,0
    
    #ORIGEN output does not give any beta decay spectrum, so only isotope predictions can be done here.
    if beta_response_type != "isotope" and beta_response_type != "none":
        print("Predict_ORIGEN called with an unsupported beta response type. It should be \"isotope\" or \"none\"")
        return 0,0
    
    if gamma_response_type == "binned":
        gamma_prediction, gamma_uncertainty = Predict_ORIGEN_binned_gamma_response(ORIGEN_filename, cooling_time_header, Binned_gamma_response_folder + fuel_type + ".txt")
        
    elif gamma_response_type == "isotope":
       gamma_prediction, gamma_uncertainty = Predict_ORIGEN_gamma_contents(ORIGEN_filename, cooling_time_header, Isotope_gamma_response_folder + fuel_type + ".txt")
        
    elif gamma_response_type == "sampled":
        gamma_prediction, gamma_uncertainty = Predict_ORIGEN_sampled_gamma_response(ORIGEN_filename, cooling_time_header, Sampled_gamma_response_folder + fuel_type + ".txt")
        
    else:
        gamma_prediction = 0
        beta_prediction = 0
    
    if beta_response_type == "isotope":
        beta_prediction, beta_uncertainty = Predict_ORIGEN_beta_contents(ORIGEN_filename, cooling_time_header, Isotope_beta_response_folder + fuel_type + ".txt")
    elif beta_response_type == "none":
        beta_prediction = 0
        beta_uncertainty = 0
        
    prediction = gamma_prediction + beta_prediction
    uncertainty = math.sqrt(gamma_uncertainty**2 + beta_uncertainty**2)
        
    return prediction, uncertainty
