from pyswip import Prolog
import pandas as pd

def get_all_characteristics(prolog):
    query_res = list(prolog.query('character(_, X)'))
    characteristcs = set()
    for res in query_res:
        for char in res['X']:
            if char not in characteristcs:
                characteristcs.add(char)
    return characteristcs

def get_characters(prolog):
    query_res = list(prolog.query('character(X, _)'))
    characters = set()
    for res in query_res:
        characters.add(res['X'])
    return characters

def get_characteristics(prolog, character):
    query_res = list(prolog.query('character(' + character + ', X)'))
    characteristics = set()
    for res in query_res:
        for char in res['X']:
            if char not in characteristics:
                characteristics.add(char)
    return characteristics

def create_df(prolog):
    characteristics = get_all_characteristics(prolog)
    characters = get_characters(prolog)
    df = pd.DataFrame(columns=characteristics, index=characters)
    for character in characters:
        query_res = list(prolog.query('character(' + character + ', X)'))
        for res in query_res:
            for char in res['X']:
                df.at[character, char] = 1
    df.fillna(0, inplace=True)
    return df


def main():
    prolog = Prolog()
    prolog.consult("qeq-db.pl")
    df = create_df(prolog)
    print(df)

if __name__ == '__main__':
    main()