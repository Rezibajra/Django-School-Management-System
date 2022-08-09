from django import forms
from django.forms import modelformset_factory
from apps.corecode.models import AcademicSession, AcademicTerm, Subject
from .models import Result
from apps.corecode.models import Mark

class CreateResults(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.filter(name__in = list(Mark.objects.all())), widget=forms.CheckboxSelectMultiple
    )


EditResults = modelformset_factory(
    Result, fields=("test_score", "exam_score", "performance_score", "speaking_score", "listening_score"), extra=0, can_delete=True
)

class EditResultsForm(EditResults):

    def __init__(self, *args, **kwargs):
        super(EditResultsForm, self).__init__(*args, **kwargs)
        if kwargs:
            data = [str(x).split()[-1] for x in kwargs['queryset']]
            for i in range(len(data)):
                data_exam = self.get_exam_score(data[i])
                data_test = self.get_test_score(data[i])
                data_performance = self.get_performance_score(data[i])
                self.forms[i].fields['exam_score'].widget.attrs.update({'min': 0, 'max': data_exam})
                self.forms[i].fields['test_score'].widget.attrs.update({'min': 0, 'max': data_test})
                self.forms[i].fields['performance_score'].widget.attrs.update({'min': 0, 'max': data_performance})

                data_speaking = self.get_speaking_score(data[i])
                data_listening = self.get_listening_score(data[i])
                self.forms[i].fields['speaking_score'].widget.attrs.update({'min': 0, 'max': data_speaking})
                self.forms[i].fields['listening_score'].widget.attrs.update({'min': 0, 'max': data_listening})

    def get_exam_score(self, subject):
        subject = Mark.objects.filter(subject__name = subject)
        if subject.values('exam_score')[0]['exam_score'] is not None:
            return int(subject.values('exam_score')[0]['exam_score'][:-1])
        else:
            return 0

    def get_test_score(self, subject):
        subject = Mark.objects.filter(subject__name = subject)
        if subject.values('test_score')[0]['test_score'] is not None:
            return int(subject.values('test_score')[0]['test_score'][:-1])
        else:
            return 0

    def get_performance_score(self, subject):
        subject = Mark.objects.filter(subject__name = subject)
        if subject.values('performance_score')[0]['performance_score'] is not None:
            return int(subject.values('performance_score')[0]['performance_score'][:-1])
        else:
            return 0
    
    def get_speaking_score(self, subject):
        subject = Mark.objects.filter(subject__name = subject)
        if subject.values('speaking_score')[0]['speaking_score'] is not None:
            return int(subject.values('speaking_score')[0]['speaking_score'][:-1])
        else:
            return 0

    def get_listening_score(self, subject):
        subject = Mark.objects.filter(subject__name = subject)
        if subject.values('listening_score')[0]['listening_score'] is not None:
            return int(subject.values('listening_score')[0]['listening_score'][:-1])
        else:
            return 0
    
            
            
        
