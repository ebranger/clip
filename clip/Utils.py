



class binned_spectrum:
    bin_edges = []
    bin_counts = []
    bin_uncertainties = []
    
    def __init__(self, edges = [], counts = [], uncertainties = []):
        self.bin_edges = edges
        self.bin_counts = counts
        self.bin_uncertainties = uncertainties
        
    def set_spectrum(self, edges, counts, uncertainties):
        self.bin_edges = edges
        self.bin_counts = counts
        self.bin_uncertainties = uncertainties
        
    def set_bin_edges(self, edges):
        self.bin_edges = edges
        
    def set_bin_counts(self, counts):
        self.bin_counts = counts
        
    def set_bin_uncertainties(self, uncertainties):
        self.bin_uncertainties = uncertainties
        
    def get_response(self):
        return self.bin_edges, self.bin_counts, self.bin_uncertainties
    
class sampled_spectrum:
    sampled_energies = []
    sampled_response = []
    sampled_uncertainties = []
    
    def __init__(self, energies = [], responses = [], uncertainties = []):
        self.sampled_energies = energies
        self.sampled_response = responses
        self.sampled_uncertainties = uncertainties
        
    def set_spectrum(self, energies, responses, uncertainties):
        self.sampled_energies = energies
        self.sampled_response = responses
        self.sampled_uncertainties = uncertainties
        
    def set_sampled_energies(self, energies):
        self.sampled_energies = energies
        
    def set_sampled_responses(self, responses):
        self.sampled_response = responses
        
    def set_sampled_uncertainties(self, uncertainties):
        self.sampled_uncertainties = uncertainties
        
    def get_response(self):
        return self.sampled_energies, self.sampled_response, self.sampled_uncertainties
    
    
class isotope_response:
    isotope_list = []
    isotope_activity_response = []
    isotope_activity_uncertainty = []
    isotope_mass_response = []
    isotope_mass_uncertainty = []
    
    def __init__(self, isotopes = [], activity_responses = [], activity_uncertainties = [], mass_responses = [], mass_uncertainties = []):
        self.isotope_list = isotopes
        self.isotope_activity_response = activity_responses
        self.isotope_activity_uncertainty = activity_uncertainties
        self.isotope_mass_response = mass_responses
        self.isotope_mass_uncertainty = mass_uncertainties
        
    def set_response(self, isotopes, activity_responses, activity_uncertainties, mass_responses, mass_uncertainties):
        self.isotope_list = isotopes
        self.isotope_activity_response = activity_responses
        self.isotope_activity_uncertainty = activity_uncertainties
        self.isotope_mass_response = mass_responses
        self.isotope_mass_uncertainty = mass_uncertainties
        
    def set_isotope_list(self, isotopes):
        self.isotope_list = isotopes
        
    def set_isotope_activity_response(self, responses):
        self.isotope_activity_response = responses
        
    def set_isotope_activity_uncertainty(self, uncertainties):
        self.isotope_activity_uncertainty = uncertainties
        
    def set_isotope_mass_response(self, responses):
        self.isotope_mass_response = responses
        
    def set_isotope_mass_uncertainty(self, uncertainties):
        self.isotope_mass_uncertainty = uncertainties
        
    def get_response(self):
        return self.isotope_list, self.isotope_activity_response, self.isotope_activity_uncertainty, self.isotope_mass_response, self.isotope_mass_uncertainty
    
    
if __name__ =="__main__":
    spectrum = binned_spectrum()
    spectrum.set_bin_edges([1,2,3,4,5])
    spectrum.set_bin_counts([10,20,30,40])
    spectrum.set_bin_uncertainties([0,0,0,0])
    
    edges, counts, uncertainties = spectrum.get_spectrum()
    
    print(edges)
    print(counts)
    print(uncertainties)
                             