import person_retriever


class UnknownPerson:
    def __init__(self, nombre):
        self.__name = nombre

    def dictify(self):
        return {
            'name': self.__name,
            'unknown': True
        }

    @property
    def name(self):
        return self.__name


class Person:
    def __init__(self, cedula):
        results = person_retriever.get_person(cedula)
        self.__id = results['cedula']
        self.__name = results['nombreCompleto']
        self.__aka = results['conocidoComo']
        self.__father_name = results['nombrePadre']
        self.__father_id = results['cedulaPadre']
        self.__mother_name = results['nombreMadre']
        self.__mother_id = results['cedulaMadre']
        self.__birth_date = results['fechaNacimiento']
        self.__nationality = results['nacionalidad']
        self.__is_dead = False if not results['difunto'] or results['difunto'] == '' else True
        if self.__is_dead:
            self.__deceased = results['difunto']

    def get_mother(self):
        if not self.__mother_id or self.__mother_id == '' or self.__mother_id == '0':
            return UnknownPerson(self.__mother_name)
        else:
            return Person(self.__mother_id)

    def get_father(self):
        if not self.__father_id or self.__father_id == '' or self.__father_id == '0':
            return UnknownPerson(self.__mother_name)
        else:
            return Person(self.__father_id)

    def dictify(self):
        return {
            'name': self.__name,
            'id': self.__id,
            'aka': self.__aka,
            'birth-date': self.__birth_date,
            'nationality': self.__nationality
        }

    @property
    def id(self):
        return self.__id

    @property
    def name(self):
        return self.__name

    @property
    def aka(self):
        return self.__aka

    @property
    def father_name(self):
        return self.__father_name

    @property
    def father_id(self):
        return self.__father_id

    @property
    def mother_name(self):
        return self.__mother_name

    @property
    def mother_id(self):
        return self.__mother_id

    @property
    def birth_date(self):
        return self.__birth_date

    @property
    def nationality(self):
        return self.__nationality

    @property
    def is_dead(self):
        return self.__is_dead

    @property
    def deceased(self):
        if self.__is_dead:
            return self.__deceased
        else:
            return False
