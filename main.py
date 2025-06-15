import json
import os
import random


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

        # Добавляем обязательных сотрудников, если их нет
        if not any(isinstance(s, ZooKeeper) for s in self.staff):
            self.add_staff(ZooKeeper("Временный смотритель"))
        if not any(isinstance(s, Veterinarian) for s in self.staff):
            self.add_staff(Veterinarian("Временный ветеринар"))

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


def add_animal_menu(zoo):
    print("\nДобавление животного:")
    print("1. Птица")
    print("2. Млекопитающее")
    print("3. Рептилия")
    choice = input("Выберите тип животного: ")

    name = input("Имя животного: ")
    age = int(input("Возраст животного: "))

    if choice == "1":
        wingspan = float(input("Размах крыльев: "))
        zoo.add_animal(Bird(name, age, wingspan))
    elif choice == "2":
        fur_color = input("Цвет шерсти: ")
        zoo.add_animal(Mammal(name, age, fur_color))
    elif choice == "3":
        scale_type = input("Тип чешуи: ")
        zoo.add_animal(Reptile(name, age, scale_type))
    else:
        print("Неверный выбор")


def add_staff_menu(zoo):
    print("\nДобавление сотрудника:")
    print("1. Смотритель")
    print("2. Ветеринар")
    choice = input("Выберите тип сотрудника: ")

    name = input("Имя сотрудника: ")

    if choice == "1":
        zoo.add_staff(ZooKeeper(name))
    elif choice == "2":
        zoo.add_staff(Veterinarian(name))
    else:
        print("Неверный выбор")


def animal_sounds(zoo):
    print("\nЗвуки животных:")
    for animal in zoo.animals:
        print(f"{animal.name} ({animal.__class__.__name__}): {animal.make_sound()}")


def random_care(zoo):
    if not zoo.animals:
        print("Нет животных для ухода")
        return

    animal = random.choice(zoo.animals)
    keeper = next((s for s in zoo.staff if isinstance(s, ZooKeeper)), None)
    vet = next((s for s in zoo.staff if isinstance(s, Veterinarian)), None)

    action = random.randint(1, 2)
    if action == 1 and keeper:
        print(keeper.feed_animal(animal))
    elif action == 2 and vet:
        print(vet.heal_animal(animal))
    else:
        print("Нет доступных сотрудников для ухода")


def main_menu(zoo):
    while True:
        print("\nМеню зоопарка:")
        print("1. Добавить животное")
        print("2. Добавить сотрудника")
        print("3. Прослушать звуки животных")
        print("4. Случайная кормёжка/уход")
        print("5. Выйти")

        choice = input("Выберите действие: ")

        if choice == "1":
            add_animal_menu(zoo)
        elif choice == "2":
            add_staff_menu(zoo)
        elif choice == "3":
            animal_sounds(zoo)
        elif choice == "4":
            random_care(zoo)
        elif choice == "5":
            break
        else:
            print("Неверный выбор")


if __name__ == "__main__":
    zoo = Zoo()
    main_menu(zoo)