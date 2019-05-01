from django.contrib import admin

from .models import (
	BillTo,
	InvoiceFor,
	Invoice
)

admin.site.register(BillTo)
admin.site.register(InvoiceFor)
admin.site.register(Invoice)