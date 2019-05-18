import datetime
from django.utils import timezone

from invoices.models import Invoice

def get_monthly_summary(instance):
	work_dataset = []
	expense_dataset = []
	total_dataset = []
	labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]

	current_year = datetime.date.today().year
	for i in range(1, 13):
		invoice_amount = 0
		expense_amount = 0
		try:
			invoices = instance.objects.filter(invoice_date__year=current_year, invoice_date__month=i)
		except:
			invoices = None

		if invoices:
			for invoice in invoices:
				invoice_amount += float(invoice.get_work_amount())
				expense_amount += float(invoice.get_expense_amount())

		total = invoice_amount + expense_amount

		work_dataset.append(invoice_amount)
		expense_dataset.append(expense_amount)
		total_dataset.append(total)


	return work_dataset, expense_dataset, total_dataset, current_year


def get_range_summary(from_date, to_date):
	from_date_split = from_date.split("/")
	to_date_split = to_date.split("/")


	# THIS AND THE CHART FOR MONTHLY BREAKDOWN DOESNT WORK!!!!!!!

	# Get all of the invoices in this range
	invoice_lower = Invoice.objects.filter(
		invoice_date__year__gte=int(from_date_split[2]),
		invoice_date__month__gte=int(from_date_split[1]),
		invoice_date__day__gte=int(from_date_split[0])
	)
	invoice_upper = Invoice.objects.filter(
		invoice_date__year__lte=int(to_date_split[2]),
		invoice_date__month__lte=int(to_date_split[1]),
		invoice_date__day__lte=int(to_date_split[0])
	)
	all_invoices = invoice_upper.intersection(invoice_lower)
	print(all_invoices)

	invoice_amount, expense_amount, total = 0, 0, 0
	# Get thet total invoice amount for these invoices
	if all_invoices:
		for invoice in all_invoices:
			invoice_amount += invoice.get_work_amount()
			expense_amount += invoice.get_expense_amount()

		total = invoice_amount + expense_amount
	return invoice_amount, expense_amount, total