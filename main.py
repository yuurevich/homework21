from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self):
        self.items = {}
        self.capacity = 0

    @abstractmethod
    def add(self, name, amount):
        pass

    @abstractmethod
    def remove(self, name, amount):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self):
        super().__init__()
        self.items = {}
        self.capacity = 100

    def add(self, name, amount):
        if name in self.items:
            self.items[name] += amount
        else:
            self.items[name] = amount

    def remove(self, name, amount):
        if self.items[name] > amount:
            self.items[name] -= amount
        else:
            del self.items[name]

    @property
    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    @property
    def get_items(self):
        return self.items

    @get_items.setter
    def get_items(self, data):
        self.items = data

    @property
    def get_unique_items_count(self):
        return len(self.items)


class Shop(Storage):
    def __init__(self):
        super().__init__()
        self.items = {}
        self.capacity = 20

    def add(self, name, amount):
        if name in self.items:
            self.items[name] += amount
        else:
            self.items[name] = amount

    def remove(self, name, amount):
        if self.items[name] > amount:
            self.items[name] -= amount
        else:
            del self.items[name]

    @property
    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    @property
    def get_items(self):
        return self.items

    @get_items.setter
    def get_items(self, data):
        self.items = data

    @property
    def get_unique_items_count(self):
        return len(self.items)


class Request:
    def __init__(self, data):
        data = data.split()
        self.from_ = data[4]
        self.to = data[5]
        self.amount = int(data[1])
        self.product = data[2]


def run_app():
    store = Store()
    shop = Shop()

    store_items = {
        'печеньки': 12,
        'конфеты': 4,
        'пряники': 5,
        'мороженое': 70
    }
    shop_items = {
        'картошка': 8,
        'помидоры': 6,
        'апельсины': 2,
    }

    store.get_items = store_items
    shop.get_items = shop_items

    try:
        while True:

            query = input('Введите запрос:   ')  # Доставить 3 печеньки со склад в магазин
                                                 # Доставить 5 картошка из магазина на склад

            if query in ['stop', 'стоп']:
                break

            request = Request(query)
            if request.from_ in 'склада':
                if request.product in store.items:  # есть ли введенный товар на складе?
                    if request.amount <= store.items[request.product]:  # достаточно ли товара находится на складе?
                        print('Нужное количество есть на складе')
                    else:
                        print('На складе недостаточно товара')
                        continue
                else:
                    print('Товара нет на складе')
                    continue

                if shop.get_unique_items_count < 5 or request.product in shop.get_items:  # есть ли свободные уникальные позиции товара?
                    if shop.get_free_space >= request.amount:  # заполнен ли магазин?
                        print(f'Курьер забрал {request.amount} {request.product} со склада')
                        print(f'Курьер везет {request.amount} {request.product} со склада в магазин')
                        print(f'Курьер доставил {request.amount} {request.product} в магазин')
                        store.remove(request.product, request.amount)
                        shop.add(request.product, request.amount)
                    else:
                        print(f'В магазине недостаточно места ({shop.get_free_space})')
                        continue
                else:
                    print('В магазине не может быть больше 5 различных товаров')
                    continue

            if request.from_ in 'магазина':
                if request.product in shop.items:  # есть ли введенный товар в магазине?
                    pass
                else:
                    print('Товара нет в магазине')
                    continue
                if request.amount <= shop.items[request.product]:  # достаточно ли товара находится в магазине?
                    print('Нужное количество есть в магазине')
                else:
                    print('В магазине недостаточно товара')
                    continue

                if store.get_free_space >= request.amount:  # заполнен ли склад?
                    print(f'Курьер забрал {request.amount} {request.product} из магазина')
                    print(f'Курьер везет {request.amount} {request.product} из магазина на склад')
                    print(f'Курьер доставил {request.amount} {request.product} на склад')
                    shop.remove(request.product, request.amount)
                    store.add(request.product, request.amount)
                else:
                    print(f'На складе недостаточно места ({store.get_free_space})')
                    continue

            print(f'На складе хранится: ({store.capacity - store.get_free_space}/{store.capacity})')
            print(*[f'{amount} {item}' for item, amount in store.get_items.items()], sep='\n')
            print()
            print(f'В магазине хранится: ({shop.capacity - shop.get_free_space}/{shop.capacity})')
            print(*[f'{amount} {item}' for item, amount in shop.get_items.items()], sep='\n')
            print()

    except:
        print('Некорректный запрос')


run_app()
