from django.db import models
from django.utils.translation import gettext_lazy as _

from vehicles.models import Vehicle
from users.models import CustomUser

class WorkOrder(models.Model):
    """
    Represents a work order.
    """
    responsible = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='work_orders_responsible',
        help_text=_("The user responsible for the work order.")
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='work_orders_created',
        help_text=_("The user who created the work order.")
    )
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.PROTECT,
        related_name='work_orders',
        help_text=_("The vehicle associated with the work order.")
    )
    issue_date_unix = models.PositiveBigIntegerField(
        _('Issue date'),
        blank=False,
        help_text=_("The issue date of the work order in Unix format.")
    )
    maintenance_type = models.CharField(
        _('Maintenance type'),
        max_length=255,
        blank=False,
        help_text=_("The type of maintenance to be performed.")
    )
    work_type = models.TextField(
        _('Work type'),
        blank=False,
        help_text=_("The type of work to be performed.")
    )

    class Meta:
        verbose_name = _("Work order")
        verbose_name_plural = _("Work orders")

    def __str__(self):
        return f'{self.vehicle}: {self.maintenance_type} - {self.work_type}'

class StatusChoices(models.TextChoices):
    """Statuses for a Work Order"""
    PENDING = 'pending', _('Pending')
    COMPLETED = 'completed', _('Completed')
    NOT_COMPLETED = 'not_completed', _('Not Completed')

class WorkOrderCompletion(models.Model):
    """
    Represents the completion of a work order.
    """

    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='completion',
        help_text=_("The work order that this completion record belongs to.")
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=StatusChoices.choices,
        default='pending',
        help_text=_("The status of the work order.")
    )
    change_registered_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='work_order_completions',
        help_text=_("The user who registered the change.")
    )
    change_date_unix = models.PositiveBigIntegerField(
        _('Change date'),
        blank=False,
        help_text=_("The date when the status was updated, in Unix format.")
    )
    responsible_notes = models.TextField(
        _('Responsible notes'),
        blank=True,
        help_text=_("Any notes from the responsible person.")
    )

    class Meta:
        verbose_name = _("Work order completion")
        verbose_name_plural = _("Work order completions")

    def __str__(self):
        return f'{self.work_order}: {self.status}'
