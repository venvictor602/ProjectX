from django.contrib import admin
from .models import CustomUser,  Product, Inventory, Order, OrderItem, Category

# Register CustomUser model with custom admin configuration
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_superuser', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser', 'is_staff', 'is_active')


# Register Product model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'stock')
    search_fields = ('name',)
    list_filter = ('price',)

# Register Inventory model
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')
    search_fields = ('product__name',)
    list_filter = ('product',)

# Register Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id',  'status', 'total_amount', 'created_at')
    search_fields = ('customer__email', 'id')
    list_filter = ('status', 'created_at')

# Register OrderItem model
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')
    search_fields = ('order__id', 'product__name')


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()

class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'company_name', 'password')
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        if user.password:  # Ensure password is hashed
            user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserCreationForm
#     model = User
#     fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('company_name',)}),)
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('username', 'email', 'company_name', 'password')}
#         ),
#     )

# admin.site.register(User, CustomUserAdmin)

admin.site.register(Category)