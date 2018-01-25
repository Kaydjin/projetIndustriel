@echo off 
echo Debut scrapping linkedin
py linkedIn_InfoPerson.py --username testgeodatas@laposte.net --password testgeodatas --keyword tours --location "san francisco bay area" --sort_by date
echo retour dans scrapping_InfoPerson.log
pause