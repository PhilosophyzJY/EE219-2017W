All the codes have been partitioned into their respective problem folder. Report provided in MS word and PDF.

Problem 1: No code was necessary here; some excel files and a simple MATLAB code to sort have been included.

Problem 2A: traintest.m is the code here; you may need some signal processing toolboxes. If you have r2016b you
should be able to run it without issue. Other files include the data needed to read in and the raw Excel files
that the plots were generated from.

Problem 2B: FOREST.py is the code here. You will need all the appropriate libraries. The raw data Excel file
has been included.

Problem 2C: NeurNetReg.m is the code here. You will need the Neural Network toolbox from MATLAB (a free 30 day trial
is available online). Screenshots of the output have been included in the report. The input data has also been included.

Problem 3: byWorkFlow.m, byPolyFitNoCV.m, and byPolyFitWithCV.m are the codes here. You will need the polyfitn toolbox
(free to download online). Beware that higher order polynomials will take years to run. They have been set to 1-3. The raw
Excel plot data and input data have also been included.

Problems 4 and 5: BosHousing.py is the code here.Please be sure to include all libraries that are referenced at the top of the
BosHousing.py file.

BosHousing.py contains a main() with the following function calls:


LinearRegs('housing_data.csv') 

PolyRegs('housing_data.csv') 

RidgeRegs('housing_data.csv') 

LassoRegs('housing_data.csv') 
RidgeVLassoVUnreg('housing_data.csv')


When running this file please be sure that only the function call of interest is uncommented while the other 4 are 
commented out.

LinearRegs and PolyRegs are used for Problem 4 while the other three are used for Problem 5.  
Each of the function calls is explained in the report.

 The raw Excel file data has been provided along with the plots.