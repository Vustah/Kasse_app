call %CONDA_PATH%\Scripts\activate.bat


cd %GLATIME_PATH%\Kasse_app\Varetelling
pip install --upgrade appjar

python Kasseprogram.py
