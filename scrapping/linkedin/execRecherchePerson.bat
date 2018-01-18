@echo off 
echo Debut scrapping linkedin
py main2.py --username testgeodatas@laposte.net --password testgeodatas --keyword tours --location "san francisco bay area" --sort_by date
echo retour dans main2.py.log
pause