call "%CONDA_PATH%\Scripts\activate.bat"


cd %GLATIME_PATH%\Varetelling
pip install --upgrade appjar

python "%GLATIME_PATH%\Varetelling\Kasseprogram.py"
