from enum import Enum
from faker import Faker


class PAYMENTS_TPYE(Enum):
    CREDIT = "credit"
    DEBIT = "debit"


class Product:
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} - {self.price}"


##############################################################################
################ Order implementation whitout single responsalbility##########


class Order:
    def __init__(self, id: int):
        self.id = id
        self.is_paid = False
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def get_amount(self):
        return sum(product.price for product in self.products)

    def get_detail(self):
        detail = "\n".join(f"product {product}" for product in self.products)
        return f"{detail}\namount: {self.get_amount()}"

    def pay(self, payment_type: str, card_number: str):
        if payment_type == PAYMENTS_TPYE.CREDIT:
            self.is_paid = True
            print(
                f"${self.get_amount()} paid order {self.id} with credit card {card_number}"
            )
        else:
            self.is_paid = True
            print(
                f"${self.get_amount()} paid order {self.id} with debit card {card_number}"
            )


def test_bad_implementation():
    fake = Faker()
    order = Order(1)
    for _ in range(10):
        name = fake.bs()
        price = fake.pyint()
        order.add_product(Product(name, price))

    card_number = fake.pyint()
    order.pay(PAYMENTS_TPYE.CREDIT, card_number)
    print(order.get_detail())


###############################################################################
#########################Apliying the single responsability####################
class OrderS:
    def __init__(self, id: int):
        self.id = id
        self.is_paid = False
        self.products = []

    def add_product(self, product: Product):
        self.products.append(product)

    def get_amount(self):
        return sum(product.price for product in self.products)

    def get_detail(self):
        detail = "\n".join(f"product {product}" for product in self.products)
        return f"{detail}\namount: {self.get_amount()}"

    def set_paid(self, is_paid: bool):
        self.is_paid = is_paid


class Payment:
    def __init__(self) -> None:
        self.id = Faker().pyint()

    def pay_credit(self, card_number: str, order: OrderS):
        order.set_paid(True)
        print(
            f"${order.get_amount()} paid order {self.id} with credit card {card_number}"
        )

    def pay_debit(self, card_number: str, order: OrderS):
        order.set_paid(True)
        print(
            f"${order.get_amount()} paid order {self.id} with debit card {card_number}"
        )


def test_single_responsability_implementation():
    fake = Faker()
    orders = OrderS(1)
    for _ in range(10):
        name = fake.bs()
        price = fake.pyint()
        orders.add_product(Product(name, price))

    card_number = fake.pyint()
    payment = Payment()
    payment.pay_debit(card_number, orders)
    print(orders.get_detail())


if __name__ == "__main__":
    test_bad_implementation()
    test_single_responsability_implementation()
