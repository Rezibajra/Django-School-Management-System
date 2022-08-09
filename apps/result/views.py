from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student
from apps.corecode.models import Mark

from .forms import CreateResults,  EditResultsForm
from .models import Result

from django.contrib.auth.mixins import PermissionRequiredMixin       #Added
from django.contrib.auth.decorators import permission_required       #Added

@login_required
@permission_required('result.add_result')                            #Added
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":

        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data["subjects"]
                session = form.cleaned_data["session"]
                term = form.cleaned_data["term"]
                students = request.POST["students"]
                results = []
                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    if stu.current_class:
                        for subject in subjects:
                            check = Result.objects.filter(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                subject=subject,
                                student=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        session=session,
                                        term=term,
                                        current_class=stu.current_class,
                                        subject=subject,
                                        student=stu,
                                    )
                                )

                Result.objects.bulk_create(results)
                return redirect("edit-results")

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            print(form)
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didnt select any student.")
    return render(request, "result/create_result.html", {"students": students})


@login_required
@permission_required('result.change_result')                           #Added
def edit_results(request):
    if request.method == "POST":
        form = EditResultsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        form = EditResultsForm(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})


class ResultListView(LoginRequiredMixin, PermissionRequiredMixin, View):     #Modified
    permission_required = "result.view_result"                               #Added
    def get(self, request, *args, **kwargs):
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        bulk = {}
        real_total = {}
        for result in results:
            test_total = 0
            exam_total = 0
            performance_total = 0
            speaking_total = 0
            listening_total = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    subjects.append(subject)
                    test_total += subject.test_score
                    exam_total += subject.exam_score
                    performance_total += subject.performance_score
                    speaking_total += subject.speaking_score
                    listening_total += subject.listening_score
                print(subjects)
            
            if result.student.id in real_total:
                real_total[result.student.id] += int(Mark.objects.filter(subject = result.subject).values('exam_score')[0]['exam_score'][:-1])
            else:
                real_total[result.student.id] = int(Mark.objects.filter(subject = result.subject).values('exam_score')[0]['exam_score'][:-1])
            
            if Mark.objects.filter(subject = result.subject).values('test_score')[0]['test_score'] is not None:
                real_total[result.student.id] += int(Mark.objects.filter(subject = result.subject).values('test_score')[0]['test_score'][:-1])

            if Mark.objects.filter(subject = result.subject).values('performance_score')[0]['performance_score'] is not None:
                real_total[result.student.id] += int(Mark.objects.filter(subject = result.subject).values('performance_score')[0]['performance_score'][:-1])

            if str(result.subject) == "English":
                if Mark.objects.filter(subject = result.subject).values('listening_score')[0]['listening_score'] is not None:
                    real_total[result.student.id] += int(Mark.objects.filter(subject = result.subject).values('listening_score')[0]['listening_score'][:-1])

                if Mark.objects.filter(subject = result.subject).values('speaking_score')[0]['speaking_score'] is not None:
                    real_total[result.student.id] += int(Mark.objects.filter(subject = result.subject).values('speaking_score')[0]['speaking_score'][:-1])

            bulk[result.student.id] = {
                "student": result.student,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "performance_total": performance_total,
                "speaking_total": speaking_total,
                "listening_total": listening_total,
                "total_total": test_total + exam_total + performance_total + speaking_total + listening_total,
                "real_total": real_total[result.student.id],
                "percentage": format(((test_total + exam_total + performance_total + speaking_total + listening_total) / real_total[result.student.id]) * 100, ".2f") + "%",
            }

        context = {"results": bulk}
        return render(request, "result/all_results.html", context)
