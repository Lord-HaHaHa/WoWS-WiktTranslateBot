import requests
from Tags import wowsTags
from Templates import *
from Links import wowsLinks
from Kapitänskills import *
from deep_translator import GoogleTranslator
import re
import sys

def updateLinks(substring):
    pos1 = -1 
    while True:
        pos1 = substring.find('[[', pos1 + 1)
        pos2 = substring.find(']]', pos1 + 1)
        if pos1 == -1:
            break
        mappingValue = substring[pos1+2:pos2]
        subList = list(substring)
        try:
            trans = wowsLinks[str(mappingValue)]
            subList[pos1+2:pos2] = trans
            substring = ''.join(subList)
        except:
            f = open("./ErrorFiles/newLinks.txt", "a", encoding="UTF8")
            f.write(mappingValue + "\n")
            f.close()
            print("ERROR WITH LINKS " + mappingValue)
    return(substring)

def updateTemplates(substring):
    pos1 = -1 
    regex = '|'.join(wowsSkipTemplates)
    while True:
        pos1 = substring.find('{{', pos1 + 1)
        pos2 = substring.find('}}', pos1 + 1)
        if pos1 == -1:
            break
        mappingValue = substring[pos1+2:pos2]
        if(len(re.findall(regex, mappingValue)) == 0):
            subList = list(substring)
            try:
                trans = wowsTemplates[str(mappingValue)]
                subList[pos1+2:pos2] = trans
                substring = ''.join(subList)
            except:
                f = open("./ErrorFiles/newTemplate.txt", "a", encoding="UTF8")
                f.write(mappingValue + "\n")
                f.close()
                print("ERROR WITH TEMPLATES")
    return(substring)

def updateKapSkills(substring):
    subList = list(substring)

    ## Entfernen der Kommentare    
    pos1 = -1
    while True:
        pos1 = substring.find('<!--', pos1 + 1)
        pos2 = substring.find('-->', pos1 + 1)
        if(pos1 == -1):
            break
        subList[pos1:pos2+3] = ""
        substring = ''.join(subList)

    #Ermittlung des Skillungstypen
    pos1 = -1
    while True:
        pos1 = substring.find('{{', pos1 + 1)
        pos2 = substring.find('\\n', pos1 + 1)
        if(pos1 == -1):
            break
        mappingValueType = substring[pos1+2:pos2]
        try:
            trans = wowsSkillTags[str(mappingValueType)]
            subList[pos1+2:pos2] = trans
            substring = ''.join(subList)
        except:
            print("ERROR - False Tag: " + mappingValueType)

    ## Austauch der Kaptän Skillungen 
    if(mappingValueType == "Commander Skills 3 BB"):
        skill = wowsSkillsBB
    elif(mappingValueType == "Commander Skills 3 CR"):
        skill = wowsSkillCR
    elif(mappingValueType == "Commander Skills 3 CV"):
        skill = wowsSkillsCV
    elif(mappingValueType == "Commander Skills 3 DD"):
        skill = wowsSkillDD

    final = ""
    for key in skill:
        pos1 = substring.find(key)
        pos2 = pos1 + len(key)
        subList= list(substring)
        trans = skill[str(key)]
        subList[pos1:pos2] = trans
        substring = ''.join(subList)
    final = final + "\n" + substring
    return(final)

def translateSection(substring):
    string = str(substring)
    # Textübersetzung via GoogleTranslate
    slices = string.split("\n")
    final = ""
    print(len(slices))
    for pice in slices:
        translated = GoogleTranslator(source='auto', target='de').translate(str(pice)) 
        if(translated != None):              
            final = final + "\n" + str(translated)
        else:
            final = final + "\n" + str(pice)
    return(final)

def translateText(substring):
    string = ""
    string = str(substring)
    final = ""
    posf1 = -1
    templates = list()
    links = list()

    # Templates Speichern
    while True:
        temp = ""
        posf1 = string.find('{{', posf1 + 1)
        posf2 = string.find('}}', posf1)
        if posf1 == -1:
            break
        temp = string[posf1:posf2+2]
        templates.append(temp)

    # Links Speichern
    while True:
        temp = ""
        posf1 = string.find('[[', posf1 + 1)
        posf2 = string.find(']]', posf1)
        if posf1 == -1:
            break
        temp = string[posf1:posf2+2]
        links.append(temp)

    # Text übersetzten
    translated = translateSection(string)

    # Orginal Template wiederherstellen
    i = 0
    while True:
        temp = ""
        posf1 = translated.find('{{', posf1 + 1)
        posf2 = translated.find('}}', posf1)
        if posf1 == -1:
            break
        translated = translated.replace(translated[posf1:posf2+2],templates[i]) 
        i = i+1

    # Orginal Links wiederherstellen
    i=0
    while True:
        temp = ""
        posf1 = translated.find('[[', posf1 + 1)
        posf2 = translated.find(']]', posf1)
        if posf1 == -1:
            break
        translated = translated.replace(translated[posf1:posf2+2],links[i]) 
        i = i+1
    
    final = translated.replace('\\n', '\n')
    return(final)

if len(sys.argv) == 2:
    print(sys.argv)
    ship = sys.argv[1]
    fileName = "./Sites/" + ship + ".txt"
    URL_en = "https://wiki.wargaming.net/api.php?action=parse&page=Ship:" + ship + "&prop=wikitext&uselang=en&format=json"

    req = requests.get(URL_en)
    reqJson = req.json()
    wikiText = ""
    
    try:
        wikiText = str(reqJson["parse"]['wikitext']['*'])
    except:
        raise ValueError("Kein Gültigen Schiffsnamen eingegeben")

    regex = "\\"+'|\\'.join(wowsTags)
    startIndexes = dict()
    for match in re.finditer(regex, wikiText):
        startIndexes.update({match.start() : match.group()})

    listStart = list()
    for i in startIndexes:
        listStart.append(i)

    i=0
    file = open(fileName, "w", encoding="UTF8")
    while(i+1 < len(listStart)):
        sectionName = startIndexes[listStart[i]]
        section = wikiText[listStart[i]+len(startIndexes[listStart[i]]):listStart[i+1]]
        print(sectionName)
        if(sectionName == "|Performance=" or True):
            if(sectionName == "|Anno="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            if(sectionName == "|Performance="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
                section = "\n{{Block|!|content=Dieser Artikel wurde Maschienell übersetzt und wurde noch nicht Reviewed}}\n" + section
            elif(sectionName == "|Pros="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Cons="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Research="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|OptimalConfiguration="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Upgrades="):
                print("Orginanl:", section, "\n")
                section = updateLinks(section)
                print("Update Links:", section, "\n")
                section = updateTemplates(section)
                print("Update Templates:", section, "\n")
                section = translateText(section)
                print("Translate:", section, "\n")
            elif(sectionName == "|Consumables="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|CommanderSkills="):
                section = updateKapSkills(section)
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
                section  = section.replace("\\n", '\n')
            elif(sectionName == "|Camouflage="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Signals="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Gallery="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Data="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|History="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|HistoryGallery="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            elif(sectionName == "|Video="):
                section = updateLinks(section)
                section = updateTemplates(section)
                section = translateText(section)
            #elif(sectionName == "|Ref="):
            #    section = updateLinks(section)
            #    section = updateTemplates(section)
            #    section = translateText(section)
            #print(sectionName, section)
            file.write(sectionName + " " + section)
        i = i + 1 
    file.close()
else:
    raise ValueError("Kein Schiffsnamen eingegeben")