import datetime

from django.db import models
from django.utils import timezone

class Person(models.Model):
	name = models.CharField(
		max_length=400,
	)

	address = models.CharField(
		max_length=400,
	)

	phone_number = models.CharField(
		max_length=20,
		default='0'
	)

	def __str__(self):
		return self.name


class BillTo(Person):
	def __str__(self):
		return self.name

	def get_name(self):
		return self.name


class InvoiceFor(Person):
	def __str__(self):
		return self.name

	def get_name(self):
		return self.name


class Invoice(models.Model):
	'''
	Invoice Base Class
	'''
	paid = models.BooleanField(
		"Paid", 
		default=False,
		blank=False,
	)

	payment_notes = models.CharField(
		"Payment Notes",
		null=True,
		blank=True,
		max_length=1000
	)

	invoice_date = models.DateField(
		"Invoice Date", 
		blank=False,
	)

	last_updated = models.DateField(
		"Last Updated", 
		blank=False, 
		auto_now=True,
	)

	job_number = models.CharField(
		max_length=100,
		blank=False, 
		default="Job",
	)

	invoice_for = models.ForeignKey(
		InvoiceFor, 
		blank=True,
		on_delete=models.CASCADE
	)

	bill_to = models.ForeignKey(
		BillTo, 
		blank=True,
		on_delete=models.CASCADE
	)
	invoice_id = models.IntegerField(
			default="-1"
		)

	
	def __str__(self):
		return "-".join(["INVOICE", str(self.invoice_date.year)[-2:], format(self.invoice_id, "04")])


	
	def set_invoice_id(self):
		invoice_list = Invoice.objects.filter(invoice_date__year=self.invoice_date.year).order_by("-id")

		# If this is the only invoice with this year
		if len(invoice_list) <= 1:
			self.invoice_id = 0
			self.save(update_fields=["invoice_id"])
			return

		# Otherwise grab the last invoice besides this one
		last_invoice = invoice_list[1]

		# If the invoice ID has already been updated
		if last_invoice.id == self.id and self.invoice_id != -1:
			return
		# Otherwise update
		else:
			self.invoice_id = last_invoice.invoice_id + 1
			self.save(update_fields=["invoice_id"])

		'''
		invoice_list = Invoice.objects.all().order_by("-id")

		# If this is the first invoice in the database
		if len(invoice_list) <= 1:
			self.invoice_id = 0
			self.save(update_fields=["invoice_id"])
			return 

		last_invoice = invoice_list[1]

		# If the invoice ID has already been updated
		if last_invoice.id == self.id and self.invoice_id != -1:
			return 
		# If this is the first invoice in a new year
		elif last_invoice.invoice_date.year < self.invoice_date.year:
			self.invoice_id = 0
			self.save(update_fields=["invoice_id"])
		else:
			self.invoice_id = last_invoice.invoice_id + 1
			self.save(update_fields=["invoice_id"])
		'''


	def get_invoice_id(self):
		return "-".join(["INVOICE", str(self.invoice_date.year)[-2:], format(self.invoice_id, "04")])

	def get_invoice_work(self):
		work_list=[]
		for work in self.work_set.all():
			work_list.append(work.get_work_description())
		return work_list

	def get_work_amount(self):
		work_amount = 0
		for work in self.work_set.all():
			work_amount += work.amount
		return work_amount

	def get_expense_amount(self):
		expense_amount = 0
		for expense in self.expense_set.all():
			expense_amount += expense.amount
		return expense_amount
	
	def get_invoicefor_name(self):
		return self.invoice_for.name

	def get_invoicefor_address(self):
		return self.invoice_for.address

	def get_billto_name(self):
		return self.bill_to.name

	def get_billto_address(self):
		return self.bill_to.address


class Work(models.Model):
	invoice = models.ForeignKey(
		Invoice, 
		blank=True,
		on_delete=models.CASCADE
	)

	description = models.TextField(
	)

	amount = models.DecimalField(
		max_digits=10,
		decimal_places=2,
	)

	def __str__(self):
		return self.description

	def get_amount(self):
		return "${}".format(self.amount)

	def get_work_description(self):
		return self.description


class Expense(models.Model):
	invoice = models.ForeignKey(
		Invoice, 
		blank=True,
		on_delete=models.CASCADE
	)

	description = models.TextField(
	)

	amount = models.DecimalField(
		max_digits=10, 
		decimal_places=2,
	)

	def __str__(self):
		return self.description

	def get_amount(self):
		return "${}".format(self.amount)

	def get_expense_description(self):
		return self.description