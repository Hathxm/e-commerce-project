from django.dispatch import Signal
from django.contrib import messages
from django.dispatch import receiver


from django.dispatch import Signal

order_created_signal = Signal()
order_cancelled_signal = Signal()

@receiver(order_created_signal)
def handle_order_created(sender,instance,request, **kwargs):
    messages.success(request, 'Order has been created.')

@receiver(order_cancelled_signal)
def handle_order_cancelled(sender, instance, request, **kwargs):
    messages.success(request, 'Order has been cancelled.')

