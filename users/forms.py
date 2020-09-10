from django import forms

class NameForm(forms.Form):
	your_name = forms.CharField(label='Your name', max_length=20)

	def __init__(self, data=None, *args, **kwargs):
		super(NameForm,self).__init__(*args, **kwargs)
		self.fields['your_name'].widget.attrs['placeholder'] = data['username']
		self.fields['your_name'].widget.attrs['autofocus'] = 'autofocus'


'''	class Meta:
		widgets = {'username': forms.TextInput(attrs={'autofocus':'autofocus'})}


	def __init__(self, *args, **kwargs):
		super(NameForm, self).__init__(*args, **kwargs)
		for key, field in self.fields.items():
			if isinstance(field.widget, forms.TextInput) or \
				isinstance(field.widget, forms.Textarea) or \
				isinstance(field.widget, forms.DateInput) or \
				isinstance(field.widget, forms.DateTimeInput) or \
				isinstance(field.widget, forms.TimeInput):
				field.widget.attrs.update({'placeholder': field.label})
'''