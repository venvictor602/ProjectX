from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q

class DepartmentPermission(BasePermission):
    """
    Custom permission class that checks if a user belongs to a specific department (group)
    and has the required permission for the action they are attempting.
    """

    # Mapping of departments to permissions for each action
    department_permissions = {
        'Sales': {
            'list_products': 'inventory.view_product',        # View products
            'list_orders': 'inventory.view_order',            # View orders
            'create_order': 'inventory.add_order',            # Add orders
            'apply_discount': 'inventory.change_order',       # Apply discounts
            'view_invoice': 'inventory.view_invoice',         # View invoices
            'create_customer': 'inventory.add_customer',      # Add customers
            'view_customers': 'inventory.view_customer',      # View customers
        },
        'Inventory Management': {
            'add_product': 'inventory.add_product',           # Add product
            'change_product': 'inventory.change_product',     # Change product
            'delete_product': 'inventory.delete_product',     # Delete product
            'view_inventory': 'inventory.view_inventory',     # View inventory levels
            'update_stock': 'inventory.update_stock',         # Update stock levels
            'add_category': 'inventory.add_category',         # Add product category
            'view_category': 'inventory.view_category',       # View product category
        },
        'Finance': {
            'view_orders': 'inventory.view_order',            # View orders
            'view_invoices': 'inventory.view_invoice',        # View invoices
            'view_discounts': 'inventory.view_discount',      # View discounts
            'manage_discounts': 'inventory.change_discount',  # Manage discounts
            'view_taxes': 'inventory.view_tax',               # View taxes
            'manage_taxes': 'inventory.change_tax',           # Manage taxes
            'view_pricing_history': 'inventory.view_pricing_history', # View pricing history
            'generate_financial_reports': 'inventory.view_financial_report', # Generate reports
        },
        'Customer Support': {
            'view_orders': 'inventory.view_order',            # View orders
            'view_customers': 'inventory.view_customer',      # View customers
            'update_order_status': 'inventory.change_order',  # Update order statuses
            'view_invoices': 'inventory.view_invoice',        # View invoices
            'issue_refunds': 'inventory.change_payment',      # Issue refunds
        }
    }

    def has_permission(self, request, view):
        # Get the department name from the user's groups (assuming one department per user)
        user_groups = request.user.groups.all()

        if not user_groups.exists():
            raise PermissionDenied("You do not belong to any department.")  # If user belongs to no department

        department_name = user_groups[0].name

        # Check if the department has a permissions mapping
        if department_name not in self.department_permissions:
            raise PermissionDenied(f"Your department ({department_name}) does not have access to this resource.")  # If no specific permissions configured for department

        # Get the required permission for the current action
        action_permissions = self.department_permissions.get(department_name, {})
        required_permission = action_permissions.get(view.action)

        # If there's no permission defined for this action, raise an error
        if required_permission is None:
            raise PermissionDenied(f"Your department ({department_name}) is not authorized to perform this action.")

        # Check if the user has the required permission
        if not request.user.has_perm(required_permission):
            raise PermissionDenied(f"You do not have the required permission to perform this action. Please contact your administrator.")

        return True  # User has permission to perform the action
