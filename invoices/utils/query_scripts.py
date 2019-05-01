import datetime
from django.utils import timezone

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


def get_summary_by_range():
	pass