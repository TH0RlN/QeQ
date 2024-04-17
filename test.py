rom pyswip import Prolog

prolog = Prolog()
prolog.consult("family.pl")

print(list(prolog.query("parent(john,X)")))