from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap_datepicker_plus import DatePickerInput
from django.db import models
from django.shortcuts import get_object_or_404
import datetime
from django.forms.widgets import Textarea


from .models import (
	Invoice, 
	Work, 
	Expense, 
)

class InvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice

		fields = [
			'invoice_date',
			'job_number',
			'invoice_for',
			'bill_to',
			'payment_notes',
			'paid',
		]
		widgets = {
			'invoice_date': DatePickerInput(format='%d/%m/%Y'),
		}


class UpdateInvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice
		fields = [
			'invoice_date',
			'job_number',
			'invoice_for',
			'bill_to',
			'payment_notes',
			'paid',
		]

		widgets = {
			'invoice_date': DatePickerInput(format='%d/%m/%Y'),
			'payment_notes': Textarea()
		}


class SelectDateRangeForm(forms.Form):
	from_date = forms.fields.DateField(
		widget=DatePickerInput(format='%d/%m/%Y')
	)
	to_date = forms.fields.DateField(
		widget=DatePickerInput(format='%d/%m/%Y')
	)

WorkFormset = forms.modelformset_factory(
	Work, 
	form=InvoiceForm,
	fields=['description', 'amount'],
	extra=1
)

ExpenseFormset = forms.modelformset_factory(
	Expense,
	form=InvoiceForm,
	fields=['description', 'amount'],
	extra=1
)

UpdateWorkFormset = forms.modelformset_factory(
	Work, 
	form=InvoiceForm,
	fields=['description', 'amount'],
	extra=0
)

UpdateExpenseFormset = forms.modelformset_factory(
	Expense,
	form=InvoiceForm,
	fields=['description', 'amount'],
	extra=0
)
