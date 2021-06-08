import json
import pandas as pd
import numpy as np
import sqlalchemy as sql


def find_number(to_search: str):
    if to_search in commentsList:
        number = commentsList[commentsList.index(to_search) - 1]
        commentsList.remove(number)
        commentsList.remove(to_search)


with open('assets/arxiv.json') as archive:
    data = json.load(archive)

relation1 = []
relation2 = []
for dictionary in data:
    numPages = '0'
    numFigures = '0'
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

    if "page" in commentsList:
        numPages = commentsList[commentsList.index("page") - 1]
        commentsList.remove(numPages)
        commentsList.remove("page")

    if "figures" in commentsList and commentsList[commentsList.index("figures") - 1] != "with":
        count = commentsList[commentsList.index("figures") - 1]
        commentsList.remove(count)
        if count == "five":
            count = "5"
        numFigures = count
        commentsList.remove("figures")

    if "figure" in commentsList:
        numFigures = commentsList[commentsList.index("figure") - 1]
        commentsList.remove(numFigures)
        commentsList.remove("figure")

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

        smallRelationDictionary = {
            "sub-category": subCategory,
            "category": category
        }

        bigRelationDictionary = {
            "id": dictionary["id"].replace(" ", ""),
            "sub-category": subCategory,
            "submitter": dictionary["submitter"].replace(" ", ""),
            "title": title,
            "pages": numPages,
            "figures": numFigures,
            "comment": comment,
            "abstract": abstract,
            "update_date": dictionary["update_date"],
            "author": dictionary["author"].replace(" ", "")
        }

        relation1.append(bigRelationDictionary)
        if smallRelationDictionary not in relation2:
            relation2.append(smallRelationDictionary)

engine = sql.create_engine('sqlite:///assets/articles.db', echo=True)
df1 = pd.DataFrame(relation1)
df2 = pd.DataFrame(relation2)
df1.to_sql('article', con=engine, if_exists='replace')
df2.to_sql('category', con=engine, if_exists='replace')

np.savetxt('assets/article.txt', df1, fmt='%s')
np.savetxt('assets/category.txt', df2, fmt='%s')

print(df1)
print(df2)