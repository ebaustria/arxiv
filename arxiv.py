import json
import pandas as pd
import numpy as np
import sqlalchemy as sql


def find_number(to_search: str) -> str:
    if to_search in commentsList:
        number = commentsList[commentsList.index(to_search) - 1]
        commentsList.remove(number)
        commentsList.remove(to_search)
        return number
    return '0'


with open('assets/arxiv.json') as archive:
    data = json.load(archive)

relation1 = []
relation2 = []
relation3 = []
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

    numPages = find_number("pages")
    if numPages == '0':
        numPages = find_number("page")

    if "figures" in commentsList and commentsList[commentsList.index("figures") - 1] != "with":
        count = commentsList[commentsList.index("figures") - 1]
        commentsList.remove(count)
        if count == "five":
            count = "5"
        numFigures = count
        commentsList.remove("figures")

    if numFigures == '0':
        numFigures = find_number("figure")

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

    article_id = dictionary["id"].replace(" ", "")

    bigRelationDictionary = {
        "id": article_id,
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

    for cat in categoriesList:
        catAndSubCat = cat.split('.')
        category = catAndSubCat[0]
        subCategory = catAndSubCat[1]

        smallRelationDictionary = {
            "sub-category": subCategory,
            "category": category
        }

        candidateKeyDictionary = {
            "id": article_id,
            "sub-category": subCategory
        }

        if smallRelationDictionary not in relation2:
            relation2.append(smallRelationDictionary)
        relation3.append(candidateKeyDictionary)

engine = sql.create_engine('sqlite:///assets/articles.db', echo=True)

df1 = pd.DataFrame(relation1)
df2 = pd.DataFrame(relation2)
df3 = pd.DataFrame(relation3)

df1.to_sql('article', con=engine, if_exists='replace', index=False)
df2.to_sql('category', con=engine, if_exists='replace', index=False)
df3.to_sql('id_subcat', con=engine, if_exists='replace', index=False)

np.savetxt('assets/article.txt', df1, fmt='%s')
np.savetxt('assets/category.txt', df2, fmt='%s')
np.savetxt('assets/id_subcat.txt', df3, fmt='%s')

print(df1)
print(df2)
print(df3)
