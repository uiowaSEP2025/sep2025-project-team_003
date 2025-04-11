from hsabackend.models.contractor import Contractor
from hsabackend.utils.pagination_service import GenericSearchPaginatedView


class ContractorsList(GenericSearchPaginatedView):
    model = Contractor
    search_fields = ["first_name__icontains", "last_name__icontains", "email__icontains", "phone__icontains"]
    default_order = 'first_name'
    page_size = 10