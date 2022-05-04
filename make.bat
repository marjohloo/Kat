pause TURN OFF VIRUS CHECKER OR EXCLUDE FOLDER
rem python -m nuitka --mingw64 --plugin-enable=tk-inter --windows-icon-from-ico=lxr.ico --include-data-file=lxr.ico=lxr.ico --include-data-dir=json=json --onefile violaceum.py
pyinstaller --clean -w --onefile Kat.py
rem copy lxr.ico dist
rem xcopy /y json\ dist\json\
pause TURN ON VIRUS CHECKER