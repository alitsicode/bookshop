from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from .models import Order
class deletemixin():
    def dispatch(self, request,pk, *args, **kwargs):
        orderuser=get_object_or_404(Order,pk=pk)
        if request.user.is_superuser or request.user == orderuser.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404(_('you cant delete this order'))