pause TURN OFF VIRUS CHECKER OR EXCLUDE FOLDER
rem python -m nuitka --mingw64 --plugin-enable=tk-inter --windows-icon-from-ico=lxr.ico --include-data-file=lxr.ico=lxr.ico --include-data-dir=json=json --onefile violaceum.py
cd images
magick kat16.png kat20.png kat24.png kat32.png kat40.png kat48.png kat60.png kat72.png kat128.png kat256.png ..\Kat.ico
magick avataaars16.png avataaars20.png avataaars24.png avataaars32.png avataaars40.png avataaars48.png avataaars60.png avataaars72.png avataaars128.png avataaars256.png ..\Kat.ico
cd ..
pyinstaller --clean -w --onefile --icon="Kat.ico" --distpath="dist\Kat" Kat.py
copy Kat.pdf dist\Kat
copy Kat.ico dist\Kat
copy LICENSE dist\Kat
cd dist
"C:\Program Files\7-Zip\7z" a -tzip Kat.zip Kat\
cd ..
pause TURN ON VIRUS CHECKER