from .models import Product, ProductImage


class ProductService:

    @staticmethod
    def create_product(validated_data):
        return Product.objects.create(**validated_data)

    @staticmethod
    def update_product(product, validated_data):

        for key, value in validated_data.items():
            setattr(product, key, value)

        product.save()
        return product

    @staticmethod
    def add_product_image(product, image, is_primary=False):

        return ProductImage.objects.create(
            product=product,
            image=image,
            is_primary=is_primary
        )