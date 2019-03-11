from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from tree.models import Branch, BranchPost
from tree.api.serializers import BranchSerializer, BranchPostSerializer
from django.shortcuts import get_object_or_404


class BranchesView(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = BranchSerializer

    def get_queryset(self):
        queryset = Branch.objects.all()

        parent_id = self.request.GET.get("parent_id")
        if parent_id:
            queryset = queryset.filter(parent_id=parent_id)
        return queryset


class BranchView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BranchSerializer
    queryset = Branch.objects.all()


class BranchPostListView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BranchPostSerializer

    def get_branch(self):
        pk = self.kwargs.get("branch_id")
        branch = get_object_or_404(Branch.objects.all(), pk=pk)
        return branch

    def get(self, *_):
        queryset = BranchPost.objects.filter(branch_id=self.kwargs.get("branch_id"))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, branch_id):
        request.data["branch_id"] = branch_id
        branch = self.get_branch()
        serializer = self.serializer_class(branch=branch, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

