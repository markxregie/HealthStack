from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm

# --- Corrected Imports ---
from .models import Patient, User
from hospital_admin.models import hospital_department, specialization
from doctor.models import Doctor_Information

class CustomUserCreationForm(UserCreationForm):
    # ... (code for this form remains the same)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control floating'})

class PatientForm(forms.ModelForm):
    # ... (code for this form remains the same)
    class Meta:
        model = Patient
        fields = ['name', 'age', 'phone_number', 'blood_group', 'featured_image', 'history', 'nid', 'dob', 'address']
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class PasswordResetForm(ModelForm):
    # ... (code for this form remains the same)
    class Meta:
        model = User
        fields = ['email']
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control floating'})

# --- The Form for Doctor Registration ---
class DoctorRegistrationForm(forms.Form):
    certificate_image = forms.FileField(required=False, label="Upload Certificate Image", widget=forms.FileInput(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(
        queryset=hospital_department.objects.none(),
        empty_label="-- Please Select a Department --",
        label="Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'This field is required. You must select a department.'}
    )
    specialization = forms.ModelChoiceField(
        queryset=specialization.objects.none(),
        empty_label="-- Please Select a Specialization --",
        label="Specialization",
        widget=forms.Select(attrs={'class': 'form-control'}),
        error_messages={'required': 'This field is required. You must select a specialization.'}
    )

    def __init__(self, *args, **kwargs):
        hospital_id = kwargs.pop('hospital_id', None)
        super().__init__(*args, **kwargs)
        if hospital_id:
            self.fields['department'].queryset = hospital_department.objects.filter(hospital_id=hospital_id)
            self.fields['specialization'].queryset = specialization.objects.filter(hospital_id=hospital_id)