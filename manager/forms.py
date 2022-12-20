from django import forms
from store.models import Product,Variation
from category.models import Category,SubCategory


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product_name','brand','description', 'price','images','category','SubCategory','is_available', 'is_featured']

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_available'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'
        self.fields['is_featured'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'
        
class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name','cat_image']

    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['category_name', 'subcat_name']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class VariationForm(forms.ModelForm):

    class Meta:
        model = Variation
        fields = ['product', 'color', 'size', 'stock', 'is_active']

    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

        self.fields['is_active'].widget.attrs['class'] = 'ml-2 mt-1 form-check-input'