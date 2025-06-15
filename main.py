import json
import os


class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        return "Некий крик/говор животного"

    def eat(self):
        return f"{self.name} кушает."

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'age': self.age
        }


class Bird(Animal):
    def __init__(self, name, age, wingspan):
        super().__init__(name, age)
        self.wingspan = wingspan

    def make_sound(self):
        return "Чик-чирик!"

    def to_dict(self):
        data = super().to_dict()
        data['wingspan'] = self.wingspan
        return data


class Mammal(Animal):
    def __init__(self, name, age, fur_color):
        super().__init__(name, age)
        self.fur_color = fur_color

    def make_sound(self):
        return "Рычание!"

    def to_dict(self):
        data = super().to_dict()
        data['fur_color'] = self.fur_color
        return data


class Reptile(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type

    def make_sound(self):
        return "Шипение!"

    def to_dict(self):
        data = super().to_dict()
        data['scale_type'] = self.scale_type
        return data


def animal_sound(animals):
    for animal in animals:
        print(f"{animal.name}: {animal.make_sound()}")


class ZooKeeper:
    def __init__(self, name):
        self.name = name

    def feed_animal(self, animal):
        return f"{self.name} кормит {animal.name}"

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name
        }


class Veterinarian:
    def __init__(self, name):
        self.name = name

    def heal_animal(self, animal):
        return f"{self.name} лечит {animal.name}"

    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'name': self.name
        }


class Zoo:
    def __init__(self, filename='zoo_data.json'):
        self.filename = filename
        self.animals = []
        self.staff = []
        self.load_zoo()

    def add_animal(self, animal):
        self.animals.append(animal)
        self.save_zoo()

    def add_staff(self, staff_member):
        self.staff.append(staff_member)
        self.save_zoo()

    def save_zoo(self):
        data = {
            'animals': [animal.to_dict() for animal in self.animals],
            'staff': [staff.to_dict() for staff in self.staff]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=4)

    def load_zoo(self):
        if not os.path.exists(self.filename):
            return

        with open(self.filename, 'r') as f:
            data = json.load(f)

        for animal_data in data['animals']:
            animal_type = animal_data['type']
            if animal_type == 'Bird':
                animal = Bird(animal_data['name'], animal_data['age'], animal_data['wingspan'])
            elif animal_type == 'Mammal':
                animal = Mammal(animal_data['name'], animal_data['age'], animal_data['fur_color'])
            elif animal_type == 'Reptile':
                animal = Reptile(animal_data['name'], animal_data['age'], animal_data['scale_type'])
            else:
                animal = Animal(animal_data['name'], animal_data['age'])
            self.animals.append(animal)

        for staff_data in data['staff']:
            staff_type = staff_data['type']
            if staff_type == 'ZooKeeper':
                staff = ZooKeeper(staff_data['name'])
            elif staff_type == 'Veterinarian':
                staff = Veterinarian(staff_data['name'])
            self.staff.append(staff)

    def list_animals(self):
        for animal in self.animals:
            print(f"{animal.__class__.__name__}: {animal.name}, {animal.age} years old")

    def list_staff(self):
        for staff in self.staff:
            print(f"{staff.__class__.__name__}: {staff.name}")

if __name__ == "__main__":
    zoo = Zoo()

    # Добавление животных
    zoo.add_animal(Bird("Птичка", 2, 10))
    zoo.add_animal(Mammal("Лёва", 5, "Golden"))
    zoo.add_animal(Reptile("Шнырятель", 3, "Smooth"))

    # Добавление сотрудников
    zoo.add_staff(ZooKeeper("Иван"))
    zoo.add_staff(Veterinarian("Доктор Петров"))

    # Вывод информации
    print("Животные в Зоопарке:")
    zoo.list_animals()

    print("\nСотрудники Зоопарка:")
    zoo.list_staff()

    print("\nВот, какие звуки издают животные в Зоопарке:")
    animal_sound(zoo.animals)

    # Ищем первого попавшегося смотрителя и ветеринара
    keeper = next((staff for staff in zoo.staff if isinstance(staff, ZooKeeper)), None)
    vet = next((staff for staff in zoo.staff if isinstance(staff, Veterinarian)), None)

    # Демонстрация работы сотрудников с проверками
    if keeper and zoo.animals:
        print(f"\n{keeper.feed_animal(zoo.animals[0])}")
    else:
        print("\nНет доступного смотрителя или животных")

    if vet and len(zoo.animals) > 1:
        print(f"{vet.heal_animal(zoo.animals[1])}")
    else:
        print("Нет доступного ветеринара или недостаточно животных")