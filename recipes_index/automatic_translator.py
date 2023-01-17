# Automatic translation script using Google Translate API
#   Takes the recipes in English folder, checks if a translation is already available in the other language folder.
#       If not, it translates the recipe and saves it in the other language folder
#   This script generates the first rough translation of the recipes,
#       which will be improved by volunteer translators using pull requests to this repository

from google.cloud import translate
from google.cloud import translate_v2 as tv2
import os

# Check if folder for the language exists, if not create it
def checkFolders(availableLanguages):
    # Iterate over the available languages
    for language in availableLanguages:
        # print(availableLanguages[language])

        # Get parent directory of script
        parentDir = os.path.dirname(os.path.realpath(__file__))
        # print(parentDir)
        folderPath = os.path.join(parentDir, language['name'])
        # print(folderPath)
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)

# Translate the recipe and save it in the destination language folder
def translateRecipe(recipe, originLanguage, destinationLanguage, originLanguageCode, destinationLanguageCode):
    # Make v3 client
    client = translate.TranslationServiceClient()

    # Get parent directory of script
    parentDir = os.path.dirname(os.path.realpath(__file__))
    # print(parentDir)
    originFolderPath = os.path.join(parentDir, originLanguage)
    # print(originFolderPath)
    destinationFolderPath = os.path.join(parentDir, destinationLanguage)
    # print(destinationFolderPath)

    # Open the recipe file
    with open(os.path.join(originFolderPath, recipe), 'r', encoding='utf-8') as f:
        """
        # Translating the whole recipe at once
        # Read the file
        recipeText = f.read()
        # print(recipeText)

        # Translate the recipe
        translatedRecipe = client.translate_text(parent=f"projects/freeopensourcerecipes/locations/global", contents=recipeText, source_language_code=originLanguageCode, target_language_code=destinationLanguageCode)
        for translation in translatedRecipe.translations:
            print("Translation: {}".format(translation.translated_text))
        """

        # Translating the recipe line by line
        # Read the file line by line
        recipeLines = f.readlines()
        # print(recipeLines)

        # Translate the recipe line by line
        translatedRecipe = client.translate_text(parent=f"projects/freeopensourcerecipes/locations/global", contents=recipeLines, mime_type=f"text/plain",source_language_code=originLanguageCode, target_language_code=destinationLanguageCode)
        # for translation in translatedRecipe.translations:
            # print("Translation: {}".format(translation.translated_text))
    
    
    # Save the translated recipe in the destination language folder
    with open(os.path.join(destinationFolderPath, recipe), 'w', encoding='utf-8') as f:
        for translation in translatedRecipe.translations:
            f.write(translation.translated_text)


# Main entry point of the script
def main(recipe, originLanguage):
    oldClient = tv2.Client()

    # Get the list of available languages and save in local variable
    print("Getting available languages...")
    availableLanguages = oldClient.get_languages()
    # print(availableLanguages)

    # Check if the folders for the other languages exist, if not create them
    print("Checking if folders for other languages exist...")
    checkFolders(availableLanguages)

    # Translate the recipe in all the other available languages
    print("Translating recipe...")
    for language in availableLanguages:
        # Skip English and Romanian
        if language['language'] == 'en' or language['language'] == 'ro':
            continue
        translateRecipe(recipe, originLanguage['name'], language['name'], originLanguage['language'], language['language'])
        print("Translated to " + language['name'] + "!")

    print("Finished translation!")


main('1.txt', {'name': 'English', 'language': 'en'})
