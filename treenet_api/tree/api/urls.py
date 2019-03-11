from django.conf.urls import url
from tree.api import views

urlpatterns = [
    url(r'^branches/$', views.BranchesView.as_view(), name="branches_list"),
    url(r'^branch/(?P<pk>\w+)/$', views.BranchView.as_view(), name="branch"),
    url(r'^branch/(?P<branch_id>\w+)/posts/$', views.BranchPostListView.as_view(), name="branch_posts"),
]
