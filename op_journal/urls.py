from django.urls import path

from .views import *

urlpatterns = [
    path('', OpJournalView.as_view(), name='op_manual'),
    path('<str:substation_slug>/', OpJournalView.as_view(), name='sub_op_journal'),
    path('op_journal/<int:pk>/', op_journal_detail, name='op_journal_detail'),
    path('op_journal/<int:pk>/edit/', op_journal_edit, name='op_journal_edit'),
    path('autocomplete/', autocomplete_view, name='autocomplete'),
    path('<str:substation_slug>/autocomplete/', autocomplete_view, name='substation_autocomplete'),
    path('<str:substation_slug>/export-records/', export_records, name='export_records'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
]
