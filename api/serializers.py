from rest_framework import serializers

from todo.models import Todo


class TodoSerializer(serializers.ModelSerializer):
    #cannot be modified or not visible to the user
    created = serializers.ReadOnlyField()
    datecompleted = serializers.ReadOnlyField()

    class Meta:
        model=Todo
        fields=['id','title', 'memo', 'created', 'datecompleted', 'important']