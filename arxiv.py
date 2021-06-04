import json
import pandas as pd
import numpy as np

with open('assets/arxiv.json') as archive:
    data = json.load(archive)

processedList = []
for dictionary in data:
    numPages = '0'
    numFigures = '0'
    numTables = '0'
    numDefinitions = '0'
    comment = str()
    commentsList = str(dictionary["comments"]).split()
    categoriesList = str(dictionary["categories"]).split()
    category = ''
    subCategory = ''
    index = 0

    while index < len(commentsList):
        commentsList[index] = commentsList[index].strip(',')
        commentsList[index] = commentsList[index].strip('.')
        index += 1

    if "pages" in commentsList:
        numPages = commentsList[commentsList.index("pages") - 1]
        commentsList.remove(numPages)
        commentsList.remove("pages")

    if "figures" in commentsList:
        numFigures = commentsList[commentsList.index("figures") - 1]
        commentsList.remove(numFigures)
        commentsList.remove("figures")

    if "tables" in commentsList:
        numTables = commentsList[commentsList.index("tables") - 1]
        commentsList.remove(numTables)
        commentsList.remove("tables")

    if "definitions" in commentsList:
        numDefinitions = commentsList[commentsList.index("definitions") - 1]
        commentsList.remove(numDefinitions)
        commentsList.remove("definitions")

    index = 0
    while index < len(commentsList):
        commentsList[index] = commentsList[index].replace('\n', '')
        index += 1

    comment = ''.join(commentsList)

    if comment == '':
        comment = 'comment'

    title = dictionary["title"].replace(" ", "")
    title = title.replace('\n', '')

    abstract = dictionary["abstract"].replace(" ", "")
    abstract = abstract.replace('\n', '')

    for cat in categoriesList:
        catAndSubCat = cat.split('.')
        category = catAndSubCat[0]
        subCategory = catAndSubCat[1]

        newDict = {
            "id": dictionary["id"].replace(" ", ""),
            "submitter": dictionary["submitter"].replace(" ", ""),
            "title": title,
            "pages": numPages,
            "figures": numFigures,
            "tables": numTables,
            "definitions": numDefinitions,
            "comment": comment,
            "category": category,
            "sub-category": subCategory,
            "abstract": abstract,
            "update_date": dictionary["update_date"],
            "author": dictionary["author"].replace(" ", "")
        }

        processedList.append(newDict)

df = pd.DataFrame(processedList)
np.savetxt('assets/table_values.txt', df, fmt='%s')

print(df)
