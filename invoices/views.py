from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django import forms
from django.views import generic
from django.urls import reverse
from datetime import datetime

from django.utils import timezone
from .utils import query_scripts


from .models import(
	Invoice, 
	BillTo, 
	InvoiceFor, 
	Work, 
	Expense,
)
from .forms import (
	InvoiceForm, 
	WorkFormset,
	ExpenseFormset,
	UpdateInvoiceForm, 
	UpdateWorkFormset,
	UpdateExpenseFormset,
	SelectDateRangeForm
)


class Index(generic.ListView):

	#TODO: Add summary of invoice amounts
	
	template_name = 'invoices/index.html'

	def get(self, request, **kwargs):
		invoices, expenses, totals, year = query_scripts.get_monthly_summary(Invoice)
		context = {
			'latest_invoice_list': Invoice.objects.order_by('-last_updated')[:10],
			'invoices': invoices,
			'expenses': expenses,
			'totals': totals,
			'year': year
		}
		return render(request, self.template_name, context)
		


class InvoiceDetailView(generic.DetailView):
	#TODO: export and save as pdf without the navbar
	#TODO: add boolean for "paid"

	model = Invoice
	template_name = 'invoices/invoice_detail.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)

		context = {
			'invoice': invoice,
		}
		return render(request, self.template_name, context)


class InvoiceListView(generic.list.ListView):

	template_name = 'invoices/invoice_list.html'

	model = Invoice
	paginate_by = 20

	def get_context_data(self):
		context = {
			'invoices': Invoice.objects.all().order_by('id')
		}
		return context


class CreateInvoiceView(generic.CreateView):

	template_name = 'invoices/create_invoice.html'

	def get(self, request):
		work_formset = WorkFormset(queryset=Invoice.objects.none())
		context = {
			'title': "Invoice Information",
			'invoice_form': InvoiceForm(),
			'work_formset': work_formset,
		}
		return render(request, self.template_name, context)
	def post(self, request):
		invoice_form = InvoiceForm(request.POST)
		
		if invoice_form.is_valid():
			invoice = invoice_form.save()
		return HttpResponseRedirect(reverse('add_work', args=(invoice.id, )))


class CreateWorkView(generic.CreateView):
	template_name = 'invoices/create_work.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		invoice.set_invoice_id()
		work_formset = WorkFormset(queryset=Invoice.objects.none())
		context = {
			'invoice_id': invoice.invoice_id,
			'work_formset': work_formset
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		work_formset = WorkFormset(request.POST)

		if work_formset.is_valid():
			invoice = get_object_or_404(Invoice, **kwargs)
			invoice.set_invoice_id()
			
			for work_form in work_formset:
				if work_form.cleaned_data.get('description') and work_form.cleaned_data.get('amount'):
					work = work_form.save(commit=False)
					work.invoice = invoice
					work.save()
			invoice.save()
		return HttpResponseRedirect(reverse('add_expense', args=(invoice.id, )))


class CreateExpenseView(generic.CreateView):
	template_name = 'invoices/create_expense.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		expense_formset = ExpenseFormset(queryset=Invoice.objects.none())
		context = {
			'invoice_id': invoice.invoice_id,
			'expense_formset': expense_formset
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		expense_formset = ExpenseFormset(request.POST)

		if expense_formset.is_valid():
			invoice = get_object_or_404(Invoice, **kwargs)
			for expense_form in expense_formset:
				if expense_form.cleaned_data.get('description') and expense_form.cleaned_data.get('amount'):
					expense = expense_form.save(commit=False)
					expense.invoice = invoice
					expense.save()
			invoice.save()
		return HttpResponseRedirect(reverse('invoice_detail', args=(invoice.id, )))


class PrintInvoiceView(generic.DetailView):
	#TODO: export and save as pdf without the navbar

	model = Invoice
	template_name = 'invoices/print_invoice.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)

		context = {
			'invoice': invoice,
		}
		return render(request, self.template_name, context)


class EditInvoiceView(CreateInvoiceView):

	template_name = 'invoices/edit_invoice.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		context = {
			'invoice': invoice,
			'invoice_form': InvoiceForm(instance=invoice)
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		form = InvoiceForm(request.POST, instance=invoice)

		if form.is_valid():
			instance = form.save()
			return HttpResponseRedirect(reverse('edit_work', args=(instance.id, )))


class EditWorkView(generic.UpdateView):
	template_name = 'invoices/edit_work.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		context = {
			'invoice': invoice,
			'work_formset': UpdateWorkFormset(queryset=invoice.work_set.all())
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		formset = UpdateWorkFormset(request.POST, queryset=invoice.work_set.all())

		if formset.is_valid():
			invoice = get_object_or_404(Invoice, **kwargs)
			for form in formset:
				if form.cleaned_data.get('description') and form.cleaned_data.get('amount'):
					work = form.save(commit=False)
					work.invoice = invoice
					work.save()
			invoice.save()
			return HttpResponseRedirect(reverse('edit_expense', args=(invoice.id, )))


class EditExpenseView(generic.UpdateView):
	template_name = 'invoices/edit_expense.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		context = {
			'invoice': invoice,
			'expense_formset': UpdateExpenseFormset(queryset=invoice.expense_set.all())
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		formset = UpdateExpenseFormset(request.POST, queryset=invoice.expense_set.all())

		if formset.is_valid():
			invoice = get_object_or_404(Invoice, **kwargs)
			for form in formset:
				if form.cleaned_data.get('description') and form.cleaned_data.get('amount'):
					expense = form.save(commit=False)
					expense.invoice = invoice
					expense.save()
			invoice.save()
			return HttpResponseRedirect(reverse('invoice_detail', args=(invoice.id, )))


class DeleteInvoiceView(generic.DetailView):

	template_name = 'invoices/invoice_delete.html'

	def get(self, request, **kwargs):
		invoice = get_object_or_404(Invoice, **kwargs)
		context = {
			'invoice': invoice,
			'pk': invoice.id,
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		get_object_or_404(Invoice, **kwargs).delete()
		msg = "Successfully deleted the invoice"
		return HttpResponseRedirect(reverse('invoice_list'))

'''
class SummaryView(generic.ListView):
	template_name = 'invoices/invoice_summary.html'

	def get(self, request, **kwargs):
		#form = SelectDateRangeForm()
		invoices, expenses, totals, year = query_scripts.get_monthly_summary(Invoice)
		context = {
			'invoices': invoices,
			'expenses': expenses,
			'totals': totals,
			'year': year,
			#'date_select_form': form
		}
		return render(request, self.template_name, context)

	#def post(self, request, **kwargs):
		#form = SelectDateRangeForm(request.POST)
		#if form.is_valid:
		#	instance = form.save()
'''
'''

class SummaryRangeView(generic.DetailView):
	template_name = 'invoices/invoice_summary_range.html'

	def get(self, request, **kwargs):

'''

class SummaryView(generic.ListView):
	template_name = 'invoices/invoice_summary.html'

	def get(self, request, **kwargs):
		form = SelectDateRangeForm()
		invoices, expenses, totals, year = query_scripts.get_monthly_summary(Invoice)
		context = {
			'invoices': invoices,
			'expenses': expenses,
			'totals': totals,
			'year': year,
			'date_select_form': form
		}
		return render(request, self.template_name, context)

	def post(self, request, **kwargs):
		form = SelectDateRangeForm(request.POST)
		if form.is_valid:
			from_date = form['from_date'].value()
			to_date = form['to_date'].value()

			return HttpResponseRedirect(
				reverse(
					'summary_range', 
					args=(from_date, to_date, )
				)
			)


class SummaryRangeView(generic.ListView):
	template_name = 'invoices/summary_range.html'

	def get(self, request, **kwargs):
		invoice, expense, total = query_scripts.get_range_summary(
			kwargs["from_date"], 
			kwargs["to_date"]
		)
		context = {
			'from_date': kwargs["from_date"],
			'to_date': kwargs["to_date"],
			'invoice_total': invoice,
			'expense_total': expense,
			'total': total
		}
		return render(request, self.template_name, context)


def SearchView(request):
	query_str = request.GET.get('query_str')
	instance = None

	if Invoice.objects.filter(id=query_str):
		instance = Invoice.objects.filter(id=query_str)[0]

	if instance:
		return HttpResponseRedirect(reverse('invoice_detail', args=(instance.pk, )))
	else:
		msg = "Sorry, no match found"
		return HttpResponseRedirect(reverse('index'))

