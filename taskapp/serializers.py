
from rest_framework.serializers import (ModelSerializer, SerializerMethodField,
                                        SlugRelatedField, CharField, ReadOnlyField)
from rest_framework.validators import UniqueTogetherValidator
from rest_framework import serializers
from taskapp.models import Role,Employee,Task,Comments

class RoleSerializer(ModelSerializer):
    class Meta:
        model = Role

class EmployeeSerializer(ModelSerializer):
    """
    Displaying Team Members in Dictionary Format
    """
    first_name = SerializerMethodField()
    last_name = SerializerMethodField()
    email = SerializerMethodField()
    role = SerializerMethodField()
    created_date = SerializerMethodField()
    modified_date = SerializerMethodField()

    class Meta:
        model = Employee
        fields = ('id', 'first_name','last_name', 'email', 'role',
                  'created_date', 'modified_date')

class TaskSerializer(ModelSerializer):

    def validate(self, data):
        """
        Check that the start is before the stop.
        """
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("end_date must be greater than start date")
        return data

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'priority','time', 'start_date',
                  'end_date','is_status')

class CommentsSerializer(ModelSerializer):

    class Meta:
        model = Comments
        exclude = ['created_by', 'updated_by']