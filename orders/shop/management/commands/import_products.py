import yaml
from django.core.management.base import BaseCommand
from shop.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter

class Command(BaseCommand):
    help = 'Import products from a YAML file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the YAML file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']
        with open(file_path, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)

        self.import_data(data)

    def import_data(self, data):
        shop_data = data.get('shop')
        categories_data = data.get('categories', [])
        goods_data = data.get('goods', [])

        # Import Shop
        shops={}
        for sh in shop_data:
            shop, _ = Shop.objects.get_or_create(id=sh['id'], name=sh['name'])
            print(f'Imported Shop: {shop.name}')

        # Import Categories
        categories = {}
        for cat in categories_data:
            category, _ = Category.objects.get_or_create(name=cat['name'])
            categories[cat['id']] = category
            print(f'Imported Category: {category.name}')

        # Import Products and ProductInfo
        for good in goods_data:
            category = categories.get(good['category'])
            if not category:
                print(f'Category ID {good["category"]} not found for Product: {good["name"]}')
                continue  # Пропустить текущую итерацию, если категория не найдена

            shop_id = good['shop']['id']
            shop = Shop.objects.filter(id=shop_id).first()
            if not shop:
                print(f'Shop ID {shop_id} not found for Product: {good["name"]}')
                continue  # Пропустить текущую итерацию, если магазин не найден

            product, _ = Product.objects.get_or_create(category=category, name=good['name'])
            print(f'Imported Product: {product.name}')

            product_info, _ = ProductInfo.objects.get_or_create(
                product=product,
                shop=shop,
                defaults={
                    'name': good['name'],
                    'quantity': good['quantity'],
                    'price': good['price'],
                    'price_rrc': good['price_rrc'],
                }
            )
            print(f'Imported ProductInfo: {product_info.name} (Shop: {product_info.shop.name})')

        # Import Parameters
        for param_name, param_value in good.get('parameters', {}).items():
            parameter, _ = Parameter.objects.get_or_create(name=param_name)
            print(f'Imported Parameter: {parameter.name}')

            ProductParameter.objects.get_or_create(
                product_info=product_info,
                parameter=parameter,
                defaults={'value': param_value}
            )
            print(f'Imported ProductParameter: {param_name} = {param_value}')