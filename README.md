# clip
Cherenkov Light Intensity Prediction for nuclear safeguards
``clip`` is a python package for estimating the Cherenkov light intensity of a spent nuclear fuel assembly for nuclear safeguards purposes. It takes as input the results of a burnup calculation, combines the relevant information with simulated data regarding the intensity of Cherenkov light produced in an assembly by various source terms, to provide a value of the relative intensity to be used in DCVD partial defect measurements of spent nuclear fuel assemblies. ``clip`` is designed to be able to read information from burnup calculations, and combine this data with fuel assembly Cherenkov light responses of a few different formats to make a prediction. The code takes into account the gamma-decays of a fuel assembly, which create the majority of the Cherenkov light, and it can also take into account the direct-beta contribution, i.e. beta decays that pass through the fuel and cladding with sufficient energy to directly produce Cherenkov light in the surrounding water.

Burnup calculations
===================

The code can read burnup files from two different codes to make predictions:
- ORIGEN-ARP, which is part of the Oak Ridge SCALE package. The code has been tested for SCALE version 6.1.
- Serpent2. The code can read gamma spectrum output files, as well as material (bumat) files. The code has been tested with Serpent2 version 2.1.0

Gamma contribution calculations
===============================

Depending on what burnup calculations were done, and on the level of accuracy that is required in the predictions, the code can make predictions for three different formats for the Cherenkov light production as a function of decay gamma energy. These three formats for the Cherenkov light response function are a binned format, a sampled format and an isotope contents format.

Binned response
---------------

For a binned response, it is expected that the gamma emission data is provided in a binned format. The binned response format must have the same bin edges as the binned gamma spectrum provided by the burnup calculation. This response format is primarily intended to be used with ORIGEN, which calculates the emission gamma spectrum of an assembly in a binned format. For Serpent, a binned response can still be used if a gamma spectrum is provided. The code will then create a binned gamma spectrum using the same binning procedure implemented in ORIGEN, and using the bin edges defined in the response data file. This response format is a trade-off between accuracy and speed, being decently fast for performing the simulations required to construct the response function, while including information about all gamma emissions from the fuel assembly.

The response function for this format is the average number of vertically directed Cherenkov photons produced within the assembly, per gamma photon with an energy from the bin. Thus, if bin number i contains <img src="https://latex.codecogs.com/gif.latex?C_i" />  counts, and the response for bin i is <img src="https://latex.codecogs.com/gif.latex?R_i" />, then the code calculates

<img src="https://latex.codecogs.com/gif.latex?\sum{C_i*R_i}" />

which is then the predicted Cherenkov light intensity of the assembly.

To create a binned response function, first the binning to be used must be specified. Next, a Monte-Carlo particle transport code such as Geant4 or MCNP is used to simulate the radiation transport within a fuel assembly geometry. The energy of the source particles in the simulations is sampled uniformly from the bin, and the simulations tallies the number of vertically directed Cherenkov photons produced within the assembly. In this way, for each bin the Cherenkov light production for a gamma decay with energy within the bin is calculated. Once all bins have been processed, the data is put into a text file, with an example such file found in ``Data/Binned_gamma_response/PWR17x17.txt``. These text files contain one header row that is ignored by the code, and then the per-bin response, one bin per line, and sorted after bin energy. Each line is a tab-separated list containing four values, the lower bin edge, the upper bin edge, the Cherenkov light intensity per decay, and the uncertainty in the intensity due to the Monte-Carlo nature of the simulations.

Sampled response
----------------

The sampled response is intended to be used when a non-binned gamma emission spectrum is available, i.e. when all the emission energies and intensities are listed. This is primarily intended to be a gamma spectrum calculated by Serpent. If this response type is called for an ORIGEN burnup calculation, the code will convert the sampled response to a binned response, having the same bin edges as the gamma spectrum found in the ORIGEN output, and then handle it as as a binned response. This response format is intended for high accuracy, but as a consequence the time required for the Monte-Carlo simulations to find the number of Cherenkov photons produced per decay is higher.

The response function for this format is the average number of vertically directed Cherenkov photons produced within the assembly, per gamma photon with a specific energy, for selected energies. The code will use this data to interpolate a response function <img src="https://latex.codecogs.com/gif.latex?R(\epsilon)" /> that gives the average number of Cherenkov photons produced for a gamma decay of energy <img src="https://latex.codecogs.com/gif.latex?\epsilon" />. Thus, if gamma decay number i has intensity <img src="https://latex.codecogs.com/gif.latex?\I_i " /> and gamma energy <img src="https://latex.codecogs.com/gif.latex?\epsilon_i" /> The total Cherenkov light intensity is then calculated by summing the contributions from all isotopes.

<img src="https://latex.codecogs.com/gif.latex?\sum{R(\epsilon_i)*I_i}" />

To create a sampled response function, a Monte-Carlo particle transport code such as Geant4 or MCNP is used to simulate the radiation transport within a fuel assembly geometry for various monoenergetic source particles. The simulation tallies the number of vertically directed Cherenkov photons produced within the assembly for that energy. The energies that need to be simulated must cover the energy range from the lowest energy that can result in CHerenkov light production, to the highest gamma energy that is expected to be encountered in the fuel assembly. The simulations must also be done at sufficiently many different energies that the response for other energies can be interpolated from the data. When the data is available, it is put into a text file, with an example such file found in ``Data/Sampled_gamma_response/PWR17x17.txt``. These text files contain one header row that is ignored, followed by one line per simulated energy, sorted by the energy. Each line is a tab-separated list containing the simulated gamma energy, the Chernkov light production and the uncertainty in the production.

Isotope response
----------------

The isotope response is intended to be used when only the isotope abundances in a fuel assembly is available. For Serpent, this when only the bumat files are available, if no gamma transport calculation was made to obtain a gamma spectrum. For ORIGEN, the isotope abundances are provided in the output files, but using the gamma spectrum to include all isotopes is preferred. This response type works well for long-cooled fuel assemblies, when only a few isotopes of relevance remains, and thus only a few select isotopes needs to be simulated to obtain a per-isotope response. However, for short-cooled fuels, or for better accuracy, all isotopes in the fuel assembly should be considered, which is preferably done with one of the other two responses.

The response function for this format is the average number of vertically directed Cherenkov photons produced within the assembly, either per decay for an isotope, or per gram of the isotope present in the assembly. Thus, if isotope number i has a total activity <img src="https://latex.codecogs.com/gif.latex?\A_i"/>, and a per-decay response of <img src="https://latex.codecogs.com/gif.latex?\R_i"/> then the Cherenkov light production for this isotope is <img src="https://latex.codecogs.com/gif.latex?\A_i*R_i"/>.  The total Cherenkov light intensity is then calculated by summing the contributions from all isotopes.

<img src="https://latex.codecogs.com/gif.latex?\sum{A_i*I_i}" />

To create an isotope response function, a Monte-Carlo particle transport code such as Geant4 or MCNP is used to simulate the radiation transport within a fuel assembly geometry for decays of the selected isotopes. The simulation tallies the number of vertically directed Cherenkov photons produced within the assembly for that isotope. The isotopes to be simulated must cover all isotopes that contribute noticeably to the Cherenkov light intensity, which typically means that they are abundant, have a relatively high activity and emit high-energy gamma rays. When the data from the per-isotope simulations are available, it is put into a text file, with an example such file found in ``Data/Isotope_gamma_response/PWR17x17.txt``. These text files contain a header row that is ignored, followed by one line per simulated isotope. Each line is a tab-separated list containing the name of the isotope, in the same format as used in the ORIGEN output, the per-decay Cherenkov light production, the uncertainty in this production, the per-mass Cherenkov light production, and the uncertainty in this production. The conversion between a per-decay and a per-mass production value is not done by the code but is done when setting up the data, and is done by using the specific activity of the isotope.

Beta contribution calculations
==============================

In principle, beta-decays can be handled in the same way as gamma decays, and thus the beta response can be binned, sampled or be per isotope. However, since neither ORIGEN or Serpent is capable of providing a beta emission spectrum, only a per-isotope response can be used. For ORIGEN, since there is only one output file containing all information, an isotope beta response can be calculated in combination with any gamma response. For Serpent, the bumat files contain the isotope masses, and beta predictions can thus only be done if a bumat file is provided. If a prediction is to be made based on per-isotope beta decays and a gamma spectrum, the gamma and beta contributions must be predicted separately, and manually added to obtain a total prediction.

Running the code
==================

The file ``Minimal_example.py`` gives an example to how to use the code. The two functions ``Predict_ORIGEN`` and ``Predict_serpent``are the functions that most users will need. These functions need to be provided with the burnup output files, the fuel assembly type (for the Cherenkov intensity simulations results), information about what source term to use and whether direct beta contribution should be included or not.

