import requests
from bs4 import BeautifulSoup
import html5lib
import pandas as pd

pokemonCovered = {}
outputFile = "pokemon.csv"
baseURL = "https://www.pokemon.com/us/pokedex"

def getMaxNumberPokemon():
    maxPokemon = 0
    
    #bulbasaur always is first
    website = requests.get(f"{baseURL}/bulbasaur")
    website_content = BeautifulSoup(website.content,"html5lib")
    
    lastPokemon = website_content.find("a",{"class":"previous"})
    
    lastPokemonNum = lastPokemon.find("span",{"class":"pokemon-number"}).text
    
    #num is in format #nnn
    return int(lastPokemonNum[1:])
    
    
def createPokeMonDataset():
    currentPokemon = "bulbasaur"
    currentNum = 1
    maxPokemon = 0
    
    #getMaxNumberPokemon
    maxPokemon = getMaxNumberPokemon()
    print(f"Scraping {maxPokemon} Pokemon")
    
    while (len(pokemonCovered)!=maxPokemon):
        print(f"Pokemon #{currentNum}")
        website = requests.get(f"{baseURL}/{currentPokemon}")
        website_content = BeautifulSoup(website.content,"html5lib")
    
        nextURL = website_content.find("a",{"class":"next"})["href"]
        pokemonName = nextURL.split("/")[-1]
        
        attributeWrapper = website_content.find("div",{"class":"dtm-type"})
        pokemonTypes = [i.text for i in attributeWrapper.find_all("a")]
        
        pokemonCovered[currentPokemon] = pokemonTypes
        
        currentPokemon = pokemonName
        currentNum+=1

        
createPokeMonDataset()

modified = {"pokemon":[],"types":[]}

for i,j in pokemonCovered.items():
    modified["pokemon"].append(i)
    modified["types"].append(j)
    
dataFrame = pd.DataFrame(modified)

dataFrame.to_csv(outputFile)
