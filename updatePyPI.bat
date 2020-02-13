cd "C:\Users\bbpat\Box Sync\PhDBackups\BP PhD Research Backup\DiaoLab\3_ProjectFiles\2_Hardware_Software\2_Software_ActiveDevelopment\PolyChemPrintv3.0\polychemprint3_pkg"
Del /A dist
Del /A build
Del /A polychemprint3.egg-info

Python setup.py sdist
Python setup.py bdist_wheel
Twine upload dist/*
echo "try 1"
pip install --no-cache-dir --pre --upgrade polychemprint3
echo "try 2"
pip install --no-cache-dir --pre --upgrade polychemprint3
echo "try 3"
pip install --no-cache-dir --pre --upgrade polychemprint3
