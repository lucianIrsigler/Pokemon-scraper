This is a simple project

The script uses requests to access the pokedex. Then scrapes the weaknesses of each pokemon.

After the weaknesses of each pokemon is scraped, the script uses pandas to export the data to an excel file.

The script is slow due to the fact each pokemon is processed sequentially. If the script were to use multithreading, then the pokemon could be scraped quicker.

To download the dependencies required:
```
pip install -r requirements.txt
```

Then to run the script:
```
python pokemonWeaknessCalculator.py
```