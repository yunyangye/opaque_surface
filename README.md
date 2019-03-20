# opaque_surface
This repository is used to identify the differences of opaque surfaces between the PNNL and OSSTD models. The steps tp do the work are listed below:
1. Put the pnnl models into PNNL folder and put the osstd models into OpenStudio_Standards.
2. Open './python_script/main.py' and insert the information of the target models.
3. Run './python_script/main.py'.
4. The results will be stored into files with the name format: 'diff-$building_type$-$climate_zone$-$template$-$branch$'.
