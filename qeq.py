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

def main():
    prolog = Prolog()
    prolog.consult("qeq-db.pl")

    print("All characters: ", get_characters(prolog))
    print("All characteristics: ", get_all_characteristics(prolog))


if __name__ == '__main__':
    main()