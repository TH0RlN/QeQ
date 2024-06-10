import os
import pandas as pd
from pyswip import Prolog

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

def get_most_common_characteristic(df):
    return df.sum(axis=0).idxmax()


def game_loop(df):
    os.system('clear' if os.name == 'posix' else 'cls')
    print("Piensa en un personaje de la siguiente lista:")
    for character in df.index:
        print(" - " + character)
    input("Presiona Enter cuando lo tengas pensado...")

    pregunta = 1
    while df.shape[0] > 1:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\033[1;30mPregunta %d\033[0;30m" % pregunta)
        print("Personajes restantes: " + str(df.shape[0]))
        for character in df.index:
            print(" - " + character)
        print("¿Tu personaje tiene la siguiente característica?")
        characteristic = get_most_common_characteristic(df)
        print(" - " + characteristic)

        answer = input("Respuesta (s/n): ")
        while answer not in ['s', 'n', 'S', 'N']:
            print("Respuesta inválida")
            answer = input("Respuesta (s/n): ")

        if answer in ['s', 'S']:
            df = df[df[characteristic] == 1]
            df.drop(columns=[characteristic], inplace=True)
        else:
            df = df[df[characteristic] == 0]
            df.drop(columns=[characteristic], inplace=True)

        pregunta += 1
    
    os.system('clear' if os.name == 'posix' else 'cls')
    print("\033[1;30mTu personaje es...\033[0;30m")
    print(" - " + df.index[0])
    print("\n\033[1;30m¡Gracias por jugar!\033[0;30m\n\n")


def main():
    prolog = Prolog()
    prolog.consult("qeq-db.pl")
    df = create_df(prolog)

    try:
        game_loop(df)
    except KeyboardInterrupt:
        os.system('clear' if os.name == 'posix' else 'cls')
        print("\033[1;30m\nHasta la próxima!\033[0;30m\n\n")


if __name__ == '__main__':
    main()