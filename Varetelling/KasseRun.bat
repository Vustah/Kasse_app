call %CONDA_PATH%\Scripts\activate.bat


cd %GLATIME_PATH%\gla-timen-sw\Varetelling
pip install --upgrade appjar

python Kasseprogram.py
