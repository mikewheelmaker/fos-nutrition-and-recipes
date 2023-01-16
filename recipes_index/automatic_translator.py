# Automatic translation script using Google Translate API
#   Takes the recipes in English folder, checks if a translation is already available in the other language folder.
#       If not, it translates the recipe and saves it in the other language folder
#   This script generates the first rough translation of the recipes,
#       which will be improved by volunteer translators using pull requests to this repository

# First install the googletrans package using the command
#   pip install googletrans
import googletrans as gt
import os

# Check if folder for the language exists, if not create it
def checkFolder(language):
    if not os.path.exists(language):
        os.makedirs(language)

# Main entry point of the script
def __main__():
    # Get the list of available languages and save in local variable
    availableLanguages = gt.LANGUAGES
    # print(availableLanguages)

    # Get parent directory of script
    parentDir = os.path.dirname(os.path.realpath(__file__))
    # print(parentDir)

    # Iterate over the available languages
    for language in availableLanguages:
        if language == 'en':
            continue
        # print(availableLanguages[language])
        folderPath = os.path.join(parentDir, availableLanguages[language])
        # print(folderPath)
        checkFolder(folderPath)

__main__()
