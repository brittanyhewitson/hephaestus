from django.urls import path, re_path

from . import views

urlpatterns = [
	path('', views.Index.as_view(), name='index'), 
	path('invoice_list/', views.InvoiceListView.as_view(), name='invoice_list'), 
	re_path(r'^(?P<pk>\d+)/$', views.InvoiceDetailView.as_view(), name='invoice_detail'), 
	path('create_invoice/', views.CreateInvoiceView.as_view(), name='create_invoice'),
	re_path(r'^add_work/(?P<pk>\d+)/$', views.CreateWorkView.as_view(), name='add_work'),
	re_path(r'^add_expense/(?P<pk>\d+)/$', views.CreateExpenseView.as_view(), name='add_expense'),
	re_path(r'edit_invoice/(?P<pk>\d+)/$', views.EditInvoiceView.as_view(), name='edit_invoice'),
	re_path(r'edit_work/(?P<pk>\d+)/$', views.EditWorkView.as_view(), name='edit_work'),
	re_path(r'edit_expense/(?P<pk>\d+)/$', views.EditExpenseView.as_view(), name='edit_expense'),
	path('invoice_summary/', views.SummaryView.as_view(), name='invoice_summary'),
	re_path(r'summary_range/(?P<from_date>\d{2,}/\d{2,}/\d{4,})/(?P<to_date>\d{2,}/\d{2,}/\d{4,})', views.SummaryRangeView.as_view(), name='summary_range'),
	re_path(r'delete_invoice/(?P<pk>\d+)/$', views.DeleteInvoiceView.as_view(), name='invoice_delete'),
	path('search/', views.SearchView, name='search'),
	re_path(r'^print_invoice/(?P<pk>\d+)/$', views.PrintInvoiceView.as_view(), name='print_invoice')
]