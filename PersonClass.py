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
    def __init__(self, datos, query=True):
        if query:
            results = person_retriever.get_person(datos)
        else:
            results = datos

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
        if 'children' in results:
            self.__children = results['children']

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
            'self': {
                'name': self.__name,
                'id': self.__id,
                'aka': self.__aka,
                'birth-date': self.__birth_date,
                'nationality': self.__nationality,
                'children': False if not hasattr(self, '_Person__children') else self.__children
            },
            'parents': {
                'father': {
                    'name': self.father_name,
                    'id': self.father_id
                },
                'mother': {
                    'name': self.mother_name,
                    'id': self.mother_id
                }
            }
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


class PersonList:
    def __init__(self, nombre='', apellido1='', apellido2=''):
        self.results = person_retriever.get_person_by_name(nombre, apellido1, apellido2)
        self.i = 0
        self.__person_list = []
        for i in range(len(self.results)):
            self.__person_list.append(Person(self.results[i], query=False))

    def __next__(self):
        try:
            index = self.results[self.i]
        except:
            raise StopIteration()
        self.i += 1
        return index

    def __iter__(self):
        return self

    def dictify(self):
        person_dict = {}
        for i in range(len(self.__person_list)):
            person_dict[i] = self.__person_list[i].dictify()
        return person_dict

    @property
    def person_list(self):
        return self.__person_list
