
import sys
import os
import math

from clip.Utils import *
from clip.read_responses import *
from clip.read_ORIGEN_output import *
from clip.Predict import *
from clip.read_serpent_output import *

default_data_folder = "Data"



class Clip:
    
    fuel_type = ""
    gamma_prediction_mode = ""
    beta_prediction_mode = ""
    burnup_calculation = ""
    burnup_file_name = ""
    ORIGEN_cooling_time_header = ""
    
    ready_to_predict = False
    
    binned_beta_responses = {}
    binned_gamma_responses = {}
    isotope_beta_responses = {}
    isotope_gamma_responses = {}
    sampled_beta_responses = {}
    sampled_gamma_responses = {}
    
    def __init__(self, data_folder = default_data_folder):
        self.load_responses(data_folder)
        self.fuel_type = ""
        self.gamma_prediction_mode = ""
        self.beta_prediction_mode = ""
        self.burnup_calculation = ""
        self.burnup_file_name = ""
        self.ORIGEN_cooling_time_header = ""
        
        self.ready_to_predict = False
        
    def load_responses(self, data_folder):
        if os.path.isdir(data_folder + "/Binned_beta_response/"):
            for file in os.listdir(data_folder + "/Binned_beta_response/"):
                filename = file[:-4] #remove the .txt
                
                #Load the data and save it.
                bin_edges, bin_count, bin_uncertainty = read_binned_response(data_folder + "/Binned_beta_response/" + file)
                data = binned_spectrum(bin_edges, bin_count, bin_uncertainty)
                self.binned_beta_responses[filename] = data
        
        if os.path.isdir(data_folder + "/Binned_gamma_response/"):
            for file in os.listdir(data_folder + "/Binned_gamma_response/"):
                filename = file[:-4] #remove the .txt
                
                #Load the data and save it.
                bin_edges, bin_count, bin_uncertainty = read_binned_response(data_folder + "/Binned_gamma_response/" + file)
                data = binned_spectrum(bin_edges, bin_count, bin_uncertainty)
                self.binned_gamma_responses[filename] = data
         
        if os.path.isdir(data_folder + "/Isotope_beta_response/"):
            for file in os.listdir(data_folder + "/Isotope_beta_response/"):
                filename = file[:-4] #remove the .txt
                
                #Load the data and save it.
                isotope_list, isotope_activity_response, isotope_activity_uncertainty = read_isotope_response(data_folder + "/Isotope_beta_response/" + file, "decay")
                isotope_list2, isotope_mass_response, isotope_mass_uncertainty = read_isotope_response(data_folder + "/Isotope_beta_response/" + file, "mass")
                
                data = isotope_response(isotope_list, isotope_activity_response, isotope_activity_uncertainty, isotope_mass_response, isotope_mass_uncertainty)
                self.isotope_beta_responses[filename] = data
        
        if os.path.isdir(data_folder + "/Isotope_gamma_response/"):
            for file in os.listdir(data_folder + "/Isotope_gamma_response/"):
                filename = file[:-4] #remove the .txt
                
                #Load the data and save it.
                isotope_list, isotope_activity_response, isotope_activity_uncertainty = read_isotope_response(data_folder + "/Isotope_gamma_response/" + file, "decay")
                isotope_list2, isotope_mass_response, isotope_mass_uncertainty = read_isotope_response(data_folder + "/Isotope_gamma_response/" + file, "mass")
                
                data = isotope_response(isotope_list, isotope_activity_response, isotope_activity_uncertainty, isotope_mass_response, isotope_mass_uncertainty)
                self.isotope_gamma_responses[filename] = data
        
        if os.path.isdir(data_folder + "/Sampled_beta_response/"):        
            for file in os.listdir(data_folder + "/Sampled_beta_response/"):
                filename = file[:-4] #remove the .txt
                
                #Load the data and save it.
                sampled_energies, response, uncertainty = read_sampled_response(data_folder + "/Sampled_beta_response/" + file)
                data = sampled_spectrum(sampled_energies, response, uncertainty)
                self.sampled_beta_responses[filename] = data
           
        if os.path.isdir(data_folder + "/Sampled_gamma_response/"):
            for file in os.listdir(data_folder + "/Sampled_gamma_response/"):
                filename = file[:-4] #remove the .txt
                
                #Load the data and save it.
                sampled_energies, response, uncertainty = read_sampled_response(data_folder + "/Sampled_gamma_response/" + file)
                data = sampled_spectrum(sampled_energies, response, uncertainty)
                self.sampled_gamma_responses[filename] = data
                
        print("Clip initialization: loaded " + str(len(self.binned_beta_responses)) + " binned beta responses.")
        print("Clip initialization: loaded " + str(len(self.binned_gamma_responses)) + " binned gamma responses.")
        print("Clip initialization: loaded " + str(len(self.isotope_beta_responses)) + " isotope beta responses.")
        print("Clip initialization: loaded " + str(len(self.isotope_gamma_responses)) + " isotope gamma responses.")
        print("Clip initialization: loaded " + str(len(self.sampled_beta_responses)) + " sampled beta responses.")
        print("Clip initialization: loaded " + str(len(self.sampled_gamma_responses)) + " sampled gamma responses.")
        
        
    def set_prediction_parameters(self, fuel, gamma, beta, burnup, ORIGEN_header = ""):

        self.load_OK = True
        
        if burnup != "ORIGEN" and burnup != "Serpent_bumat" and burnup != "Serpent_gamma":
            print("Asked for a prediction based on a burnup calculation from: " + burnup + ". Supported outputs are ORIGEN, Serpent_bumat and Serpent_gamma.")
            self.load_OK = False
        else:
            self.burnup_calculation = burnup
            if burnup == "ORIGEN":
                if ORIGEN_header != "":
                    self.ORIGEN_cooling_time_header = ORIGEN_header
                else:
                    print ("ORIGEN prediciton requested, but no cooling time header was provided.")
                    self.load_OK = False
        
        if gamma != "binned" and gamma != "sampled" and gamma != "isotope" and gamma != "none":
            print("Asked for a gamma response of type: " + str(gamma) + ". Supported responses are binned, sampled, isotope or none.")
            self.load_OK = False
        else:
            self.gamma_prediction_mode = gamma
            
        if beta != "isotope" and beta != "none":
            print("Asked for a beta response of type: " + str(beta) + ". Supported responses are isotope or none.")
            self.load_OK = False
        else:
            self.beta_prediction_mode = beta
            
        if gamma == "binned":
            if fuel in self.binned_gamma_responses:
                self.fuel_type = fuel
            else:
                print("Asked for a binned gamma response for fuel: " + str(fuel) + ", but no such response was found in the loaded responses.")
                self.load_OK = False
            
        if beta == "binned":
            if fuel in self.binned_beta_responses:
                self.fuel_type = fuel
            else:
                print("Asked for a binned beta response for fuel: " + str(fuel) + ", but no such response was found in the loaded responses.")
                self.load_OK = False
            
            
        if gamma == "sampled":
            if fuel in self.sampled_gamma_responses:
                self.fuel_type = fuel
            else:
                print("Asked for a sampled gamma response for fuel: " + str(fuel) + ", but no such response was found in the loaded responses.")
                self.load_OK = False
            
        if beta == "sampled":
            if fuel in self.sampled_beta_responses:
                self.fuel_type = fuel
            else:
                print("Asked for a sampled beta response for fuel: " + str(fuel) + ", but no such response was found in the loaded responses.")
                self.load_OK = False
            
        if gamma == "isotope":
            if fuel in self.isotope_gamma_responses:
                self.fuel_type = fuel
            else:
                print("Asked for an isotope gamma response for fuel: " + str(fuel) + ", but no such response was found in the loaded responses.")
                self.load_OK = False
            
        if beta == "isotope":
            if fuel in self.isotope_beta_responses:
                self.fuel_type = fuel
            else:
                print("Asked for an isotope beta response for fuel: " + str(fuel) + ", but no such response was found in the loaded responses.")
                self.load_OK = False
            
        if self.load_OK == False:
            self.burnup_calculation = ""
            self.gamma_prediction_mode = ""
            self.beta_prediction_mode = ""
            self.burnup_calculation = ""
            print("Cannot make predictions for the selected response type and burnup calculation")
        else:
            self.ready_to_predict = True
        
    def predict(self, filename):
        
        gamma_prediction = 0
        gamma_uncertainty = 0
        beta_prediction = 0
        beta_uncertainty = 0
        
        if self.burnup_calculation == "ORIGEN":
            if self.gamma_prediction_mode == "binned":
                
                #Load data
                spectrum_edges, spectrum_counts = read_ORIGEN_gamma_spectrum(filename, self.ORIGEN_cooling_time_header) 
                response_edges, response_counts, response_uncertainties = self.binned_gamma_responses[self.fuel_type].get_response()
    
                #Check that data has been loaded
                if len(spectrum_edges) == 1 or len(response_edges) == 1:
                    print("Failed in loading data for ORIGEN binned response prediction")
                    gamma_prediction, gamma_uncertainty = 0,0
                    
                #Check that bin structure matches.
                if len(spectrum_edges) != len(response_edges):
                   print("Different bin structure for the gamma emissions and the simulated response")
                   gamma_prediction, gamma_uncertainty = 0,0
                    
                for i in range(0,len(spectrum_edges)):
                   if spectrum_edges[i] != response_edges[i]:
                       print("Different bin structure for the gamma emissions and the simulated response")
                       gamma_prediction, gamma_uncertainty = 0,0
                        
                #Uncertainty in gamma spectrum not provided by ORIGEN, so do not include here.
                spectrum_uncertainties = [0] * len(spectrum_counts)    
                gamma_prediction, gamma_uncertainty = Predict_binned_response(spectrum_counts, spectrum_uncertainties, response_counts, response_uncertainties)
            
            elif self.gamma_prediction_mode == "sampled":
                
                #Load data
                spectrum_edges, spectrum_counts = read_ORIGEN_gamma_spectrum(filename, self.ORIGEN_cooling_time_header) 
                sampled_energies, sampled_response, sampled_uncertainties = self.sampled_gamma_responses[self.fuel_type].get_response()
                
                #Convert from sampled response to the binning used in the ORIGEN gamma spectrum
                binned_response = get_binned_response_function(sampled_energies, sampled_response, spectrum_edges)
                binned_response_uncertainties = get_binned_response_function(sampled_energies, sampled_uncertainties, spectrum_edges)
                  
                #Uncertainty in gamma spectrum not provided by ORIGEN, so do not include here.
                spectrum_uncertainties = [0] * len(spectrum_counts)    
                gamma_prediction, gamma_uncertainty = Predict_binned_response(spectrum_counts, spectrum_uncertainties, binned_response, binned_response_uncertainties)    
            
            elif self.gamma_prediction_mode == "isotope":
                
                isotope_list, unused1, unused2, response, response_uncertainty = self.isotope_gamma_responses[self.fuel_type].get_response()
    
                #read the isotope_list that we have a response for.
                isotope_mass_contents = read_ORIGEN_isotope_contents(filename, self.ORIGEN_cooling_time_header, isotope_list)
            
                #ORIGEN provides no uncertainties on each isotope mass, so neglect this 
                #uncertainty contribution for now.
                isotope_uncertainties = [0] * len(isotope_mass_contents)  
                gamma_prediction, gamma_uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)
            
            if self.beta_prediction_mode == "isotope":
                
                #Read all isotopes for which we have a respone defined
                isotope_list, unused1, unused2, response, response_uncertainty = self.isotope_beta_responses[self.fuel_type].get_response()
                
                #read the isotope_list that we have a response for.
                isotope_mass_contents = read_ORIGEN_isotope_contents(filename, self.ORIGEN_cooling_time_header, isotope_list)
            
                #ORIGEN provides no uncertainties on each isotope mass, so neglect this 
                #uncertainty contribution for now.
                isotope_uncertainties = [0] * len(isotope_mass_contents)  
                beta_prediction, beta_uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)
                                                    
            prediction = gamma_prediction + beta_prediction
            uncertainty = math.sqrt(gamma_uncertainty**2 + beta_uncertainty**2)
                
            return prediction, uncertainty
            
        if self.burnup_calculation == "Serpent_gamma":
            if self.gamma_prediction_mode == "binned":
                spectrum_energies, spectrum_counts = read_serpent_gamma_spectrum(filename)
                response_edges, response_counts, response_uncertainties = self.binned_gamma_responses[self.fuel_type].get_response()
                
                ORIGEN_binned_spectrum = convert_to_ORIGEN_binning(spectrum_energies, spectrum_counts, response_edges)
                
                #Uncertainty in gamma spectrum not provided by serpent, so do not include here.
                ORIGEN_binnned_uncertainties = [0] * len(ORIGEN_binned_spectrum)    
                gamma_prediction, gamma_uncertainty = Predict_binned_response(ORIGEN_binned_spectrum, ORIGEN_binnned_uncertainties, response_counts, response_uncertainties)    
                
            elif self.gamma_prediction_mode == "sampled":
                spectrum_energies, spectrum_counts = read_serpent_gamma_spectrum(filename)
                sampled_energies, sampled_response, sampled_uncertainties = self.sampled_gamma_responses[self.fuel_type].get_response()
                
                #Uncertainties not provided by Serpent gamma spectrum output
                spectrum_uncertainties = [0] * len(spectrum_energies)
                
                gamma_prediction, gamma_uncertainty = Predict_sampled_response(spectrum_energies, spectrum_counts, spectrum_uncertainties, sampled_energies, sampled_response, sampled_uncertainties)
            elif self.gamma_prediction_mode == "isotope":
                print("Prediction requisted for Serpent_gamma, but an isotope response was requested.")
                print("Serpent_gamma can be used with a binned or a sampled response.")
                return 0,0
            
            
            if self.beta_prediction_mode != "none":
                print("Beta prediction requiested for Serpent_gamma burnup results, no beta data is available")
                print("Beta predictions require a Serpent_bumat burnup result.")
                return 0,0           

            prediction = gamma_prediction + beta_prediction
            uncertainty = math.sqrt(gamma_uncertainty**2 + beta_uncertainty**2)
                
            return prediction, uncertainty 
            
        if self.burnup_calculation == "Serpent_bumat":
            if self.gamma_prediction_mode == "isotope":
                isotope_list, unused1, unused2, response, response_uncertainty = self.isotope_gamma_responses[self.fuel_type].get_response()
    
                #read the isotope_list that we have a response for.
                isotope_mass_contents = read_serpent_isotope_contents(filename, isotope_list)
                
                #Serpent provides no uncertainties on each isotope mass, so neglect this 
                #uncertainty contribution for now.
                isotope_uncertainties = [0] * len(isotope_mass_contents)  
                gamma_prediction, gamma_uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)
            else:
                print ("Prediction based on a Serpent_bumat burnup calculation requested, only isotope response function can be used.")
                print("The requested response function was: " + str(self.gamma_prediction_mode))
                return 0,0

            if self.beta_prediction_mode == "isotope":
                isotope_list, unused1, unused2, response, response_uncertainty = self.isotope_beta_responses[self.fuel_type].get_response()
    
                #read the isotope_list that we have a response for.
                isotope_mass_contents = read_serpent_isotope_contents(filename, isotope_list)
                
                #Serpent provides no uncertainties on each isotope mass, so neglect this 
                #uncertainty contribution for now.
                isotope_uncertainties = [0] * len(isotope_mass_contents)  
                beta_prediction, beta_uncertainty = Predict_isotope_response(isotope_mass_contents, isotope_uncertainties, response, response_uncertainty)
            elif self.beta_prediction_mode == "none":
                beta_prediction = 0
                beta_uncertainty = 0
            else:
                  print("Requested prediction with beta contribution: " + str(self.beta_prediction_mode) + ", but only isotope supported.")
                  return 0,0
                

            prediction = gamma_prediction + beta_prediction
            uncertainty = math.sqrt(gamma_uncertainty**2 + beta_uncertainty**2)
                
            return prediction, uncertainty 
        
    def set_ORIGEN_cooling_time(self, header):
        self.ORIGEN_cooling_time_header = header
            
            
            
            
            
            
            
            
            
            
            
            
            
            