from django.contrib.auth import login, authenticate
class TodoCompletedList(generics.ListAPIView):
    serializer_class = TodoSerializer
    #make sure the user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        objects_filter = Todo.objects.filter(user=user, datecompleted__isnull=False).order_by("-datecompleted")
        return objects_filter
