@echo off 
echo Debut scrapping linkedin
py linkedIn_Recherche.py --username testgeodatas@laposte.net --password testgeodatas --keyword tours --location "san francisco bay area" --sort_by date
echo retour dans scrapping_Recherche.log
pause