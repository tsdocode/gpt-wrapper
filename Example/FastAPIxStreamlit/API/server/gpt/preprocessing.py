
from random import uniform, choice
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()


start , end, schema, question, code = '<|startoftext|>\n' , '\n<|endoftext|>\n' , '[SCHEMA]:' , '\n[QUESTION]:' , '\n[SQL]:'

def make_sample(s, q, c):
    return start + schema + s + question + q  + code + c + end


def replace_var(question_ , sql, var):
    for v in var:
        if not var[v].isnumeric():
            sql = sql.replace(f'= "{v}"', f'LIKE "%{var[v]}%"')
            sql = sql.replace(f'= {v}', f'LIKE "%{var[v]}%"')
        else:
            sql = sql.replace(v, var[v])
        question_ = question_.replace(v, var[v])

        return question_, sql

def remove_alias(sql):
    sql = sql.replace('TABLEalias0.', '')
    sql = sql.replace('AS TABLEalias0', '')
    return sql

def random_or(sql, question):
    if "AND" in sql:
        p = uniform(0, 1)
        if p > 0.5:
            sql = sql.replace("AND", "OR")
            question = question.replace("and", "or")
    return sql, question


def findSynm(word): 
    synonyms = []
    antonyms = []
    
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                 antonyms.append(l.antonyms()[0].name())
                    
    return synonyms

def wordTokenize(word):
    return nltk.word_tokenize(word)

def lemma(word):
    return lemmatizer.lemmatize(word)


custom_ner = ['skype' , 'email']

def to_upper_entity(question , columns):
    print('RAW QUESTION : ' , question)
    question = question.lower()
    tokens =  wordTokenize(question)
    
    columns = [col.split(':')[0].lower().strip() for col in columns]
    print("QUESTION TOKENS : " , tokens)
    synm = {}
    for col in columns:
        synm[col] = findSynm(col)
        if '_' in col:
            synm[col].extend(col.split('_'))
            synm[col].extend([" ".join(col.split('_'))])
        else:
            synm[col].extend([col])
    print("COLUMNS SYMN: " , synm)
    for col in columns:
        for syn in synm[col]:
            if f"{syn} " in question:
                question = question.replace(f"{syn} " , f"{col.upper()} ")
                break
    print("#"*10)
    return question

    
    

