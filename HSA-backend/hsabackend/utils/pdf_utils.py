from decimal import Decimal
from fpdf import FPDF
from hsabackend.models.job_service import JobService
from hsabackend.models.job import Job
from hsabackend.utils.string_formatters import format_currency
from hsabackend.models.job_material import JobMaterial

def get_job_detailed_table(pdf:FPDF, job:Job):
    grey = 215
    pdf.set_x(10)
    with pdf.table(
        line_height=5,
        padding=2,
        text_align=("LEFT",) * 5,
        borders_layout="SINGLE_TOP_LINE",
        cell_fill_color=grey,
        cell_fill_mode="ROWS",
    ) as tbl:
        hdr = tbl.row()
        hdr.cell("Services Rendered", colspan=2, align="C")
        for svc in JobService.objects.select_related("service").filter(job=job):
            info = svc.get_service_info_for_detailed_invoice()
            row = tbl.row()
            row.cell(info["service name"])
            row.cell(info["service description"])
        
        row = tbl.row()
        row.cell("Hourly Rate")
        row.cell(format_currency(job.hourly_rate))

        row = tbl.row()
        row.cell("Total Hours")
        row.cell(str(round(job.minutes_worked / 60, 2)))

        row = tbl.row()
        row.cell("Flat Rate")
        row.cell(format_currency(job.flat_fee))

        labor_cost = (
            job.hourly_rate * (Decimal(job.minutes_worked) / Decimal(60))
            + job.flat_fee
        )
        row = tbl.row()
        row.cell("Labor Cost", colspan=1)
        row.cell(format_currency(labor_cost))
    pdf.ln(5)

    # Materials table
    with pdf.table(
        line_height=5,
        padding=2,
        text_align=("LEFT",) * 4,
        borders_layout="SINGLE_TOP_LINE",
        cell_fill_color=grey,
        cell_fill_mode="ROWS",
    ) as tbl:
        hdr = tbl.row()
        hdr.cell("Material Name")
        hdr.cell("Per Unit")
        hdr.cell("Units Used")
        hdr.cell("Total")

        total = Decimal(0)
        for mat in JobMaterial.objects.filter(job=job):
            info = mat.invoice_material_row()
            r = tbl.row()
            r.cell(info["material name"])
            r.cell(format_currency(info["per unit"]))
            r.cell(str(info["units used"]))
            total += info["total"]
            r.cell(format_currency(info["total"]))

        tr = tbl.row()
        tr.cell("Materials Total")
        tr.cell("", colspan=2)
        tr.cell(format_currency(total))

        grand = total + labor_cost
        gr = tbl.row()
        gr.cell("Grand Total")
        gr.cell("", colspan=2)
        gr.cell(format_currency(grand))