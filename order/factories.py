# Importa a biblioteca factory_boy para criação de fábricas de objetos
import factory

# Importa o modelo User padrão do Django para autenticação
from django.contrib.auth.models import User

# Importa a fábrica de produtos (definida em outro arquivo)
from product.factories import ProductFactory

# Importa o modelo Order que será associado à fábrica
from order.models import Order


# Define uma fábrica para criar objetos User
class UserFactory(factory.django.DjangoModelFactory):
    # Gera um e-mail aleatório usando o Faker
    email = factory.Faker('pystr')
    # Gera um nome de usuário aleatório usando o Faker
    username = factory.Faker('pystr')
    
    # Classe de configuração/metadados da fábrica
    class Meta:
        # Especifica que esta fábrica cria instâncias do modelo User do Django
        model = User
        

# Define uma fábrica para criar objetos Order (pedidos)
class OrderFactory(factory.django.DjangoModelFactory):
    # Cria automaticamente um User relacionado usando UserFactory
    user = factory.SubFactory(UserFactory)
    
    # Método especial para tratamento de relacionamento many-to-many
    @factory.post_generation
    def product(self, create, extracted, **kwargs):
        """
        Método executado após a criação do objeto:
        - self: instância do pedido sendo criado
        - create: flag indicando se o objeto deve ser persistido no banco
        - extracted: lista de produtos que podem ser passados na criação
        - kwargs: argumentos adicionais
        """
        # Se não for para criar (apenas build), retorna sem fazer nada
        if not create:
            return
        
        # Se produtos foram fornecidos durante a criação
        if extracted:
            # Adiciona cada produto ao pedido
            for product in extracted:
                self.product.add(product)
                
    # Classe de configuração/metadados da fábrica
    class Meta:
        # Especifica que esta fábrica cria instâncias do modelo Order
        model = Order
