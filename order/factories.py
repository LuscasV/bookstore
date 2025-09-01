import factory
from django.contrib.auth.models import User
from product.factories import ProductFactory
from order.models import Order


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")

    class Meta:
        model = User


class OrderFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)
        else:
            # Caso não seja passado nenhum produto, cria um por padrão
            product = ProductFactory()
            self.product.add(product)

    class Meta:
        model = Order
