# Generated by Django 2.1.2 on 2018-11-14 04:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_auto_20181114_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='bill_to',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='invoices.BillTo'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_for',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='invoices.InvoiceFor'),
        ),
    ]
