'''from django import forms
from .models import HousekeepingTask, BaseUserProfile

class HousekeepingTaskForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(
        queryset=BaseUserProfile.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Assigned to',
        to_field_name='given_name',  # Display the given_name in the choices
    )

    class Meta:
        model = HousekeepingTask
        fields = '__all__'''