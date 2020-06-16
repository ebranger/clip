
from clip.Predict import Predict_ORIGEN
from clip.Predict import Predict_serpent
from clip.rescale import scale_serpent_to_origen

from clip.Clip import *

if __name__ == '__main__':

    #Create a predictor
    predictor = Clip()
    
    #Set default prediction parameters.
    #The first parameter is the fuel type, which must match the data files in the data folders.
    #The second is the gamma prediction mode, which can be "binned", "sampled", "isotope" or "none"
    #The third is the beta prediction mode, which can be "isotope" or "none"
    #The fourth is the burnup calculation performed, which can be "ORIGEN", "Serpent_gamma" or "Serpent_bumat"
    #The fifth (optional) is the cooling time for the ORIGEN output, the program will look for colums having this header.
    predictor.set_prediction_parameters("PWR17x17", "binned", "none", "ORIGEN", "10.0 y")
    
    #Make a prediction for one fuel
    prediction, uncertainty = predictor.predict("Example_ORIGEN_outputs/PWR_50MWd_test.out")    
    
    print("ORIGEN prediction and uncertainty for the example PWR17x17 fuel, 10 years cooling time:")
    print(prediction)
    print(uncertainty)
    print("")
    
    #Set a new cooling time for the ORIGEN predictions:
    predictor.set_ORIGEN_cooling_time("20.0 y")
    
    #Make a prediction for one fuel
    prediction, uncertainty = predictor.predict("Example_ORIGEN_outputs/PWR_50MWd_test.out")    
    
    print("ORIGEN prediction and uncertainty for the example PWR17x17 fuel, 20 years cooling time:")
    print(prediction)
    print(uncertainty)
    print("")
    
    
    #To be able to compare an ORIGEN and a Serpent gamma prediction, we must scale the results based on the simualted volume in Serpent
    spectrum_scale = scale_serpent_to_origen(0.508958) #Simulated volume of fuel was 0.508958 cm^3 in the example run. The value can be found at the end of the file.
    
    #Make a prediction for a Serpent gamma file. Note that the beta contribution cannot be assessed based on a gamma spectrum!
    predictor.set_prediction_parameters("PWR17x17", "sampled", "none", "Serpent_gamma")
    prediction, uncertainty = predictor.predict("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m") 
    prediction = prediction * spectrum_scale
    uncertainty = uncertainty * spectrum_scale
    
    print("Serpent gamma prediction and uncertainty for the example PWR17x17 fuel, 10 years cooling time:")
    print(prediction)
    print(uncertainty)
    print("")
    
    #Serpent Bumat predictions are already scaled with a volume of 1 cm^3.
    spectrum_scale = scale_serpent_to_origen(1.0) #Simulated volume of fuel was 0.508958 cm^3
    
    #And one prediction for a bumat file. Here the beta contribution can be included as "isotope"
    predictor.set_prediction_parameters("PWR17x17", "isotope", "isotope", "Serpent_bumat")
    prediction, uncertainty = predictor.predict("Example_Serpent_outputs/PWR_50MWd_10years.bumat")   
    prediction = prediction * spectrum_scale
    uncertainty = uncertainty * spectrum_scale
    
    print("Serpent bumat prediction and uncertainty for the example PWR17x17 fuel, 10 years cooling time:")
    print(prediction)
    print(uncertainty)
    print("")

