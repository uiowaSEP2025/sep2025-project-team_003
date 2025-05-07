from hsabackend.models.job import Job



def get_jobs_for_invoice(invoice_id):
    jobs = Job.objects.filter(invoice__pk=invoice_id).all()
    query = []
    for job in jobs:
        query.append(job.pk)
    return query