from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from bootstrap_datepicker_plus import DatePickerInput
from django.db import models
from django.shortcuts import get_object_or_404
import datetime


from .models import (
	Invoice, 
	Work, 
	Expense, 
)

class InvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice

		fields = '__all__'
		widgets = {
			'invoice_date': forms.SelectDateWidget(
				years=range(2010, 2030),
				empty_label=('year', 'month', 'day')
			), 
		}


class UpdateInvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice
		fields = [
			'invoice_date',
			'job_number',
			'invoice_for',
			'bill_to',
			'paid'
		]

		widgets = {
			'invoice_date': forms.SelectDateWidget(
				years=range(2010, 2030),
				empty_label=('year', 'month', 'day')
			),
		}


class SelectDateRangeForm(forms.Form):
	from_date = forms.fields.DateField(
		widget=forms.SelectDateWidget(
			years=range(2018, datetime.date.today().year+1),
			empty_label=('year', 'month', 'day')
		)
	)
	to_date = forms.fields.DateField(
		widget=forms.SelectDateWidget(
			years=range(2018, datetime.date.today().year+1),
			empty_label=('year', 'month', 'day')
		)
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
