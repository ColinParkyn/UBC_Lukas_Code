# UBC_Lukas_Code
Ke26XXA.py and hp816x_instr are wrappers for drivers from https://www.tek.com/source-measure-units/2635a-software/ivi-com-driver-series-2600a-2600b-system-sourcemeters-ke26xxa-iv
and https://www.keysight.com/main/software.jspx?cc=CA&lc=fre&nid=-11143.0.00&id=112417. The wrappers are placed in the lightlab/equipment/lab_instruments.

Colin_Lightlab_functions stores functions for a variety of sweeps such as photo current or wavelength-optical power. The sweep functions are made from simple functions from lightlab and the wrappers allowing for easy translation to other hardware.

The entire procedure of setting up is as follows. Install 32 bit anaconda, NI VISA, as well as hp816x and Ke26XXA base drivers. In the 32 bit anaconda’s cmd prompt install lightlab and comtypes as well as jupyter notebook. If you wish to set up a remote server you need to install NI’s remote visa server as well as it’s gpib ethernet wizard but if your computer is directly connected to the instruments that isn't nessecary. After that import the two wrapper .py files into the site-packages/lightlab/equipment/lab_instruments. Then open up the jupyter notebook and run each cell sequentially. 
