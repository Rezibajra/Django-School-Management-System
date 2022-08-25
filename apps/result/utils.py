from django.contrib import messages
from apps.students.models import Student
from apps.corecode.models import AcademicTerm
from .models import Result, FinalResult
from ..corecode.models import Mark

def score_grade(score):
    if score <= 10:
        return "A"

def get_term_data(term_name, session, student, subject):
    term_id = int(AcademicTerm.objects.filter(name = term_name).first().id)
    term_mark = Result.objects.filter(
        session=session,
        term=term_id,
        current_class=student.current_class,
        subject=subject,
        student=student,
    ).first()

    if term_mark is not None:
        term_mark_final = term_mark.equivalent_score
    else:
        term_mark_final = 0
    return term_mark_final

def calc_mark_by_weightage(term_weightage, term_mark):
    final_mark = (term_weightage/100) * float(term_mark)
    return final_mark

def final_result_data(request, subjects, term, session, students):
    bulk = {}
    results = []
    for student in students.split(","):
        stu = Student.objects.get(pk=student)
        total = 0
        real_total = 0
        final_term_data = AcademicTerm.objects.filter(name = "Final Result").values()
        first_term_weightage = int(final_term_data[0]['first_weightage'][:-1])
        second_term_weightage = int(final_term_data[0]['second_weightage'][:-1])
        third_term_weightage = int(final_term_data[0]['third_weightage'][:-1])
        if stu.current_class:
            subject_dict = {}
            for subject in subjects:
                subject_dict[subject.name] = {}

                first_term = "First Term"
                first_term_mark = get_term_data(first_term, session, stu, subject)

                second_term = "Second Term"
                second_term_mark = get_term_data(second_term, session, stu, subject)

                third_term = "Third Term"
                third_term_mark = get_term_data(third_term, session, stu, subject)

                first_final_mark = calc_mark_by_weightage(first_term_weightage, first_term_mark)
                second_final_mark = calc_mark_by_weightage(second_term_weightage, second_term_mark)
                third_final_mark = calc_mark_by_weightage(third_term_weightage, third_term_mark)
                all_term_total = first_final_mark + second_final_mark + third_final_mark

                subject_dict[subject.name]['first'] = first_final_mark
                subject_dict[subject.name]['second'] = second_final_mark
                subject_dict[subject.name]['third'] = third_final_mark
                subject_dict[subject.name]['all'] = all_term_total
                total += all_term_total
                real_total += 100

                results.append(
                    FinalResult(
                        session=session,
                        term=term,
                        current_class=stu.current_class,
                        subject=subject,
                        student=stu,
                        first=first_final_mark,
                        second=second_final_mark,
                        third=third_final_mark,
                        total=all_term_total,
                    )
                )

            bulk[student] = {
                "student": stu,
                "subjects": subject_dict,
                "percentage": str(format((total/real_total) * 100, ".2f")) + "%",
                "first_weightage": str(first_term_weightage) + "%",
                "second_weightage": str(second_term_weightage) + "%",
                "third_weightage": str(third_term_weightage) + "%",
                "total": total,
                "real_total": real_total
            }

        else:
            messages.warning(request, f"Result not generated for student {stu} as no class is assigned.")

    FinalResult.objects.bulk_create(results)  
    return bulk

def return_score(subject, exam_sc, test_sc, perf_sc, listen_sc, speak_sc):
    
    subject = Mark.objects.filter(subject__name = subject)
    if subject.values('exam_score')[0]['exam_score'] is not None:
        exam_score = int(subject.values('exam_score')[0]['exam_score'][:-1])
    else:
        exam_score = 0

    if subject.values('test_score')[0]['test_score'] is not None:
        test_score = int(subject.values('test_score')[0]['test_score'][:-1])
    else:
        test_score = 0

    if subject.values('performance_score')[0]['performance_score'] is not None:
        performance_score = int(subject.values('performance_score')[0]['performance_score'][:-1])
    else:
        performance_score = 0

    if subject.values('speaking_score')[0]['speaking_score'] is not None:
        speaking_score = int(subject.values('speaking_score')[0]['speaking_score'][:-1])
    else:
        speaking_score = 0

    if subject.values('listening_score')[0]['listening_score'] is not None:
        listening_score = int(subject.values('listening_score')[0]['listening_score'][:-1])
    else:
        listening_score = 0

    full_score = exam_score + test_score + performance_score + speaking_score + listening_score
    equiv_score = format(((exam_sc + test_sc + perf_sc + listen_sc + speak_sc)/full_score)*100, ".2f")
    return full_score, equiv_score
