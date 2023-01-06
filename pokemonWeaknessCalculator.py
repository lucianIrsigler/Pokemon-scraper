"""
Scrapes data from https://www.pokemon.com/us/pokedex.

Looks at the weaknesses of every pokemon.

After scraping the weaknesses of every pokemon, this data is exported to
an excel sheet.
"""


import requests
import html5lib
import pandas as pd
from bs4 import BeautifulSoup


pokemonCovered = {}
outputFile = "pokemon.csv"
baseURL = "https://www.pokemon.com/us/pokedex"


"""
    Returns the number of pokemon in the pokedex

    Returns:
        maxNum(int): Number of pokemon in the pokedex
"""
def getMaxNumberPokemon()->int:
    maxNum=0

    #bulbasaur always is first
    website = requests.get(f"{baseURL}/bulbasaur")
    website_content = BeautifulSoup(website.content,"html5lib")
    
    lastPokemon = website_content.find("a",{"class":"previous"})
    
    lastPokemonNum = lastPokemon.find("span",{"class":"pokemon-number"}).text
    
    maxNum = int(lastPokemonNum[1:])

    #num is in format #nnn
    return maxNum
    

"""
    Scrapes data and inserts data into a dictionary

    Returns:
        None
"""    
def createPokemonDataset():
    #bulbasaur is always first
    currentPokemon = "bulbasaur"
    currentNum = 1
    maxPokemon = 0
    
    #get number of pokemon in pokedex
    maxPokemon = getMaxNumberPokemon()

    print(f"Scraping {maxPokemon} Pokemon")
    
    while (len(pokemonCovered)!=maxPokemon):
        print(f"Pokemon #{currentNum}")
        website = requests.get(f"{baseURL}/{currentPokemon}")

        #parses web page
        website_content = BeautifulSoup(website.content,"html5lib")
    
        #get next pokemon
        nextURL = website_content.find("a",{"class":"next"})["href"]
        pokemonName = nextURL.split("/")[-1]
        
        attributeWrapper = website_content.find("div",{"class":"dtm-type"})

        #get weaknesses
        pokemonTypes = [i.text for i in attributeWrapper.find_all("a")]
        
        #insert into dictionary
        pokemonCovered[currentPokemon] = pokemonTypes
        
        currentPokemon = pokemonName
        currentNum+=1

def main():
    createPokemonDataset()

    modified = {"pokemon":[],"types":[]}

    #reorders the dictionary
    for i,j in pokemonCovered.items():
        modified["pokemon"].append(i)
        modified["types"].append(j)
    
    #craetes a dataframe
    dataFrame = pd.DataFrame(modified)

    #exports the data to an excel sheet
    dataFrame.to_csv(outputFile)

if __name__=="__main__":
    main()