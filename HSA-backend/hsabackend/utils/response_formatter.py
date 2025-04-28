def response_formatter(request, object_type):
    dictionary = {}
    match object_type:
        case "job":
            temp_contractors = request.data.get("contractors")
            temp_services = request.data.get("services")
            temp_materials = request.data.get("materials")

            contractors = []
            services = []
            materials = []

            for contractor in temp_contractors:
                contractors.append({
                    "id": contractor.get("id"),
                    "first_name": contractor.get("firstName"),
                    "last_name": contractor.get("lastName"),
                    "email": contractor.get("email"),
                    "phone": contractor.get("phone"),
                })
            for service in temp_services:
                services.append({
                    "id": service.get("id"),
                    "fee": service.get("fee"),
                })

            dictionary = {
                "job_status": request.data.get("jobStatus"),
                "start_date": request.data.get("startDate"),
                "end_date": request.data.get("endDate"),
                "description": request.data.get("description"),
                "organization": request.organization.id,
                "customer_id": request.data.get("customerId"),
                "job_city": request.data.get("city"),
                "job_state": request.data.get("state"),
                "job_zip": request.data.get("zip"),
                "job_address": request.data.get("address"),
            }
