pause TURN OFF VIRUS CHECKER OR EXCLUDE FOLDER
rem python -m nuitka --mingw64 --plugin-enable=tk-inter --windows-icon-from-ico=lxr.ico --include-data-file=lxr.ico=lxr.ico --include-data-dir=json=json --onefile violaceum.py
pyinstaller --clean -w --onefile --distpath="dist\Kat" Kat.py
copy Kat.pdf dist\Kat
copy LICENSE dist\Kat
cd dist
"C:\Program Files\7-Zip\7z" a -tzip Kat.zip Kat\
cd ..
pause TURN ON VIRUS CHECKER