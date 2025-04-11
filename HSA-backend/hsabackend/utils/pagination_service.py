from django.core.paginator import Paginator
from django.apps import apps
from django.db.models import Model, QuerySet, Q
from typing import Type, Optional, List
from django.db.models.fields import CharField, TextField


class PaginationService:
    def __init__(self, page_size: int = 10):
        self.page_size = page_size

    def get_searchable_fields(self, model: Type[Model]) -> List[str]:
        """Get all character and text fields that can be searched."""
        return [
            field.name for field in model._meta.fields
            if isinstance(field, (CharField, TextField))
        ]

    def build_search_query(self, search_term: str, search_fields: List[str]) -> Q:
        """Build Q objects for searching multiple fields."""
        q_objects = Q()

        if search_term:
            for field in search_fields:
                q_objects |= Q(**{f"{field}__icontains": search_term})

        return q_objects

    def get_paginated_data(
            self,
            model: Type[Model],
            page: int = 1,
            page_size: Optional[int] = None,
            filters: dict = None,
            search_term: str = None,
            search_fields: List[str] = None,
            queryset: QuerySet = None,
            order_by: str = None
    ):

        fields = [
            {
                'name': field.name,
                'verbose_name': field.verbose_name,
                'type': field.get_internal_type()
            }
            for field in model._meta.fields
        ]
        """
        Get paginated and searched data.

        Args:
            model: Django model class
            page: Page number
            page_size: Items per page
            filters: Dictionary of filters to apply
            search_term: Term to search for
            search_fields: List of fields to search in (if None, all character fields will be searched)
            queryset: Optional pre-filtered queryset
            order_by: Field to order by (prefix with '-' for descending)
        """
        if queryset is None:
            queryset = model.objects.all()

        # Apply filters
        if filters:
            queryset = queryset.filter(**filters)

        # Apply search if search term is provided
        if search_term:
            if not search_fields:
                search_fields = self.get_searchable_fields(model)

            search_query = self.build_search_query(search_term, search_fields)
            queryset = queryset.filter(search_query)

        # Apply ordering
        if order_by:
            queryset = queryset.order_by(order_by)

        # Remove duplicates if any
        queryset = queryset.distinct()

        paginator = Paginator(queryset, page_size or self.page_size)

        try:
            current_page = paginator.page(page)
        except Exception as e:
            return {
                'error': str(e),
                'data': [],
                'total_items': 0,
                'total_pages': 0,
                'current_page': page
            }

        return {
            'data': list(current_page.object_list.values()),
            'total_items': paginator.count,
            'total_pages': paginator.num_pages,
            'current_page': current_page.number,
            'fields': fields
        }


# View implementation:
from django.http import JsonResponse
from django.views import View


class GenericSearchPaginatedView(View):
    model = None
    page_size = 10
    search_fields = None  # Define in subclass or all character fields will be searched
    default_order = None

    def get(self, request, *args, **kwargs):
        if not self.model:
            return JsonResponse({'error': 'Model not specified'}, status=400)

        # Get parameters from request
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', self.page_size))
        search_term = request.GET.get('search', '')
        order_by = request.GET.get('order_by', self.default_order)

        # Get filters from query params
        filters = request.GET.dict()
        # Remove special parameters
        for param in ['page', 'page_size', 'search', 'order_by']:
            filters.pop(param, None)

        pagination_service = PaginationService()
        result = pagination_service.get_paginated_data(
            model=self.model,
            page=page,
            page_size=page_size,
            filters=filters,
            search_term=search_term,
            search_fields=self.search_fields,
            order_by=order_by,
        )

        return JsonResponse(result)


# # Example usage:
# class UserListView(GenericSearchPaginatedView):
#     model = User
#     search_fields = ['username', 'email', 'first_name', 'last_name']
#     page_size = 15
#     default_order = '-date_joined'