from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (OpJournalView, add_comment, autocomplete_view,
                    autofill_form_view, export_records, op_journal_detail,
                    op_journal_edit)

urlpatterns = [
    path('', OpJournalView.as_view(), name='op_manual'),
    path('<str:substation_slug>/',
         OpJournalView.as_view(),
         name='sub_op_journal'),
    path('op_journal/<int:pk>/',
         op_journal_detail,
         name='op_journal_detail'),
    path('op_journal/<int:pk>/edit/',
         op_journal_edit,
         name='op_journal_edit'),
    path('<str:substation_slug>/autocomplete/',
         autocomplete_view,
         name='substation_autocomplete'),
    path('<str:substation_slug>/export-records/',
         export_records,
         name='export_records'),
    path('add_comment/<int:post_id>/',
         add_comment,
         name='add_comment'),
    path('<str:substation_slug>/autofill_form/',
         autofill_form_view,
         name='autofill_form'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
