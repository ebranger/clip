# clip
Cherenkov Light Intensity Prediction for nuclear safeguards

``clip`` is a python package for estimating the Cherenkov light intensity of a spent nuclear fuel assembly for nuclear safeguards purposes. It takes as input the results of a burnup calculation, combines the relevant information with simualted data regarding the intensity of Cherenkov light produced in an assembly by various source terms, to provide a value of the relative intensity to be used in DCVD partial defect measurements of spent nucler fue assemblies.

The code is capable of making predictions based on three different assembly source term simulations:
- For a binned gamma source. This is intended to be used with an ORIGEN-ARP calculated binned gamma spectrum.
- For a sampled gamma source, where the Cherenkov light production has been evaluated for monoenergetic gamma sources of various energies. This is intended to be used for a non-binned gamma spectrum.
- For an isotope source. This is intended for when data of the abundance of selected radionuclides are available.

The code can use burnup files from two different codes:
- ORIGEN-ARP, which part of the Oak Ridge SCALE package. The code has been tested for SCALE version 6.1.
- Serpent2. The code can read gamma spectrum source files, as well as material files. The code has been tested with Serpent2 version 2.1.0

The file ``Minimal_example.py`` gives an example to how to use the code. The two functions ``Predict_ORIGEN`` and ``Predict_serpent``are the functions that most users will need. These functions need to be provided the burnup output files, the fuel assembly type (for the Cherenkov intensity simuations results), information about what source term to use and whether direct beat contrigution should be included or not.
