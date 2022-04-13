import re
# import spacy
from difflib import SequenceMatcher
from sql_metadata import Parser


def get_columns(SQL):
    return Parser(SQL).columns

def fixBlank(sql):
    blank = re.findall("(?<=\%)(.*?)(?=\%)", sql)
    for content in blank:
        sql = sql.replace(content ,  content.strip())
    return sql

def queryToAll(sql):
    cols = re.findall("(?<=SELECT\s).*(?=\sFROM)", sql)
    for col in cols:
        sql = sql.replace(col ,  "*")
       
    print(cols)
      
    return sql
    
    
def removeSpace(sql):
    return re.sub(' +', ' ', sql)

def removeField(sql):
    while 'field' in sql:
        sql = sql.replace('_field' , '')
       
    
    return sql


function_list = ['MAX', 'MIN', 'AVG', 'COUNT', 'SUM']

    
def snake_to_normal(text):
    return " ".join(text.split('_'))
    
def check_simmilar(word , other):
    ratio = SequenceMatcher(None, word, other).ratio()
    return ratio    

def col_matching(query_cols, raw_cols, sql):
    data_cols = [snake_to_normal(c) for c in raw_cols]
    for query_col in query_cols:
        col_vote = []
        for data_col in data_cols:
            ratio = check_simmilar(query_col , data_col)
            col_vote.append(ratio)
        print(f'{query_col} : ' , col_vote)
        voting = max(col_vote)
        print(voting)
        if (voting > 0.5):
            index = col_vote.index(voting)
            sql = sql.replace(f" {query_col.upper()} " , f" {raw_cols[index]} ")
            print(sql)
            query_cols[query_cols.index(query_col)] = raw_cols[index] 
    
    return sql

def toFullDistinct(sql):
    print(sql)
    if "MIN" in sql or "MAX" in sql or "AVG" in sql or "SUM" in sql or "DISTINCT" in sql:
        return sql
    elif " COUNT(" in sql:
        col = re.findall("(?<=COUNT).*(?=\sFROM)", sql)[0][1:-1]
    else:
        col = re.findall("(?<=SELECT\s).*(?=\sFROM)", sql)[0]
    
    return sql.replace(col , f'DISTINCT {col}', 1)

def remove_where(sql , question):
    if len(question.split()) < 3:
        return sql[:sql.find('WHERE')]
    else:
        return sql

def to_pretty(sql = 'SELECT a FROM b WHERE c'):
    sql = sql.replace('FROM' , '\nFROM')
    sql = sql.replace('WHERE' , '\nWHERE')
    return sql


def post_pipeline(schema, question, sql):
    if "SELECT" not in sql:
        sql = "SELECT " + sql
    sql = remove_where(sql, question)
    sql = fixBlank(sql)
    sql = removeSpace(sql)
    sql = removeField(sql)
    sql = toFullDistinct(sql)
    
    sql_cols = [item.lower() for item in get_columns(sql)]
    raw_cols = [col.split(':')[0].strip().lower() for col in schema]
    
    print(raw_cols)
    print(sql_cols)
    
    sql  = col_matching(sql_cols , raw_cols, sql)
    
    return sql

if __name__== '__main__':
    question = "hello  d d d dd d d"
    sql = """
    SELECT STUDEN FROM TABLE WHERE SCOR > 5 AND STUDENT LIKE "aa";
    """
    schema = ["student: text" , "score: number"]
    sql = post_pipeline(schema, question, sql)
    
    print(sql)

        
    

    
    
    