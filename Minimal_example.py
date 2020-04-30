
from clip.Predict import Predict_ORIGEN
from clip.Predict import Predict_serpent
from clip.rescale import scale_serpent_to_origen

if __name__ == '__main__':

    #Make an ORIGEN prediction for a binned response function and no beta contribution    
    prediction, uncertainty = Predict_ORIGEN("Example_ORIGEN_outputs/PWR_50MWd_test.out", "10.0 y", "PWR17x17", "binned", "none")
    print(prediction)
    print(uncertainty)
    
    spectrum_scale = scale_serpent_to_origen(0.508958) #Simulated volume of fuel was 0.508958 cm^3

    #Make a Serpent prediction for a binne response and no beta contribution
    prediction, uncertainty = Predict_serpent("Example_Serpent_outputs/PWR_50MWd_10years_gamma.m", "PWR17x17", "spectrum", "binned", "none")
    prediction = prediction * spectrum_scale
    uncertainty = uncertainty * spectrum_scale
    print(prediction)
    print(uncertainty)

        

