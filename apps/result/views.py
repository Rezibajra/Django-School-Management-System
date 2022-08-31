import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View
from django.contrib.auth.models import Group

from apps.students.models import Student
from apps.corecode.models import Mark

from .forms import CreateResults,  EditResultsForm
from .models import Result, FinalResult
from .utils import final_result_data, return_score, get_formatted_data

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
                lower_term = str(request.current_term).lower()
                if 'final' in lower_term:
                    final_data = final_result_data(request, subjects, term, session, students)
                    return render(
                        request,
                        "result/final_result_page.html",
                        {"data": final_data}
                    )
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
                subject_list = [str(sub.id) for sub in subjects]
                post = request.POST.copy()
                post.update({'subjects':','.join(subject_list)})
                request.session['temp_data'] = post
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
    lower_term = str(request.current_term).lower()
    if 'final' in lower_term:
        return render(
            request,
            "result/disable_update.html",
        )
    if request.method == "POST":
        form = EditResultsForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            for obj in form.deleted_objects:
                obj.delete()
            for res in result:
                res.full_score = return_score(res.subject, res.exam_score, res.test_score, res.performance_score, res.listening_score, res.speaking_score)[0]
                res.equivalent_score = return_score(res.subject, res.exam_score, res.test_score, res.performance_score, res.listening_score, res.speaking_score)[1]
                res.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
    else:
        subjects = request.session['temp_data']['subjects'].split(',')
        students = request.session['temp_data']['students'].split(',')
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term, 
            student__in = students, subject__in = subjects
        )
        form = EditResultsForm(queryset=results)
    return render(request, "result/edit_results.html", {"formset": form})


class ResultListView(LoginRequiredMixin, PermissionRequiredMixin, View):     #Modified
    permission_required = "result.view_result"                               #Added
    def get(self, request, *args, **kwargs):
        lower_term = str(request.current_term).lower()
        if 'final' in lower_term:
            if request.user.is_staff or request.user.groups.filter(name="Teacher"):
                final_results = FinalResult.objects.filter(
                    session=request.current_session, term=request.current_term
                )
            else:
                final_results = FinalResult.objects.filter(
                    session=request.current_session, term=request.current_term, student=Student.objects.get(id = request.user.member_id)
                )
                
            formatted_final_res = get_formatted_data(final_results)
            context = {"data": formatted_final_res}
            return render(request, "result/final_result_page.html", context)

        if request.user.is_staff:
            results = Result.objects.filter(
                session=request.current_session, term=request.current_term
            )
        else:
            results = Result.objects.filter(
                session=request.current_session, term=request.current_term, student=Student.objects.get(id = request.user.member_id)
            )
        bulk = {}
        for result in results:
            test_total = 0
            exam_total = 0
            performance_total = 0
            speaking_total = 0
            listening_total = 0
            equivalent_total = 0
            real_total = 0
            subjects = []

            for subject in results:
                if subject.student == result.student:
                    subjects.append(subject)
                    test_total += subject.test_score
                    exam_total += subject.exam_score
                    performance_total += subject.performance_score
                    speaking_total += subject.speaking_score
                    listening_total += subject.listening_score
                    equivalent_total += subject.equivalent_score
                    real_total+= 100
            
            bulk[result.student.id] = {
                "student": result.student,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "performance_total": performance_total,
                "speaking_total": speaking_total,
                "listening_total": listening_total,
                "total_total": test_total + exam_total + performance_total + speaking_total + listening_total,
                "equivalent_total": equivalent_total,
                "percentage": format((equivalent_total/real_total)*100, ".2f") + "%"
            }

        context = {"results": bulk}
        return render(request, "result/all_results.html", context)
