from rest_framework import serializers
from rest_framework.reverse import reverse

from api.serializers import UserPublicSerializer
from products.models import Product
from products.validators import validate_title_no_hello, unique_product_title


class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk', read_only=True)
    title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    related_products = UserProductInlineSerializer(
        source='user.product_set.all', read_only=True, many=True)  # another way to bring in another model
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail', lookup_field='pk')
    title = serializers.CharField(
        validators=[validate_title_no_hello, unique_product_title])
    name = serializers.CharField(source='title', read_only=True)

    class Meta:
        model = Product
        fields = [
            'owner',
            'url',
            'edit_url',
            'pk',
            'title',
            'name',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'related_products',
        ]

    # Can define own customised update & create method

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("product-edit", kwargs={"pk": obj.pk}, request=request)

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
