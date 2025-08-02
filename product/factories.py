# Importa a biblioteca factory_boy para criação de fábricas de objetos
import factory 

# Importa o modelo Product do aplicativo product
from product.models import Product
# Importa o modelo Category do aplicativo product
from product.models import Category


# Define uma fábrica para criar objetos Category
class CategoryFactory(factory.django.DjangoModelFactory):
    # Gera um título aleatório usando o Faker
    title = factory.Faker('pystr')
    # Gera um slug aleatório usando o Faker
    slug = factory.Faker('pystr')
    # Gera uma descrição aleatória usando o Faker
    description = factory.Faker('pystr')
    # Gera um valor booleano aleatório (True ou False) para o campo active
    active = factory.Iterator([True, False])
    
    # Classe de configuração/metadados da fábrica
    class Meta:
        # Especifica que esta fábrica cria instâncias do modelo Category
        model = Category
    

# Define uma fábrica para criar objetos Product
class ProductFactory(factory.django.DjangoModelFactory):
    # Gera um preço aleatório usando o Faker (um número inteiro)
    price = factory.Faker('pyint')
    # Cria uma categoria usando a CategoryFactory, mas de forma lazy (quando necessário)
    category = factory.LazyAttribute(CategoryFactory)
    # Gera um título aleatório usando o Faker
    title = factory.Faker('pystr')
    
    # Método especial para tratamento de relacionamento many-to-many
    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        """
        Método executado após a criação do objeto:
        - self: instância do produto sendo criado
        - create: flag indicando se o objeto deve ser persistido no banco
        - extracted: lista de categorias que podem ser passadas na criação
        - kwargs: argumentos adicionais
        """
        # Se não for para criar (apenas build), retorna sem fazer nada
        if not create:
            return
        # Se categorias foram fornecidas durante a criação
        if extracted:
            # Adiciona cada categoria ao produto
            for category in extracted:
                self.category.add(category)

    # Classe de configuração/metadados da fábrica
    class Meta:
        # Especifica que esta fábrica cria instâncias do modelo Product
        model = Product
