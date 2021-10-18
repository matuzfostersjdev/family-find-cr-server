import PersonClass

yo = PersonClass.Person('208380025')
ma = yo.get_mother()
pa = ma.get_father()

print(pa.deceased)

exit()
