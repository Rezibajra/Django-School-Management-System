from django.contrib import messages
from apps.students.models import Student
from apps.corecode.models import AcademicTerm
from .models import Result

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
        term_mark_final = term_mark.equivalent_score()
    else:
        # term_mark_final = f"Please enter the marks for {subject} for {term_name}."
        term_mark_final = 0
    return term_mark_final

def calc_mark_by_weightage(term_name, term_mark):
    term_weightage = int(AcademicTerm.objects.filter(name = term_name).first().weightage[:-1])
    final_mark = (term_weightage/100) * float(term_mark)
    return final_mark

def final_result_data(request, subjects, session, students):
    bulk = {}
    for student in students.split(","):
        stu = Student.objects.get(pk=student)
        total = 0
        real_total = 0
        if stu.current_class:
            subject_dict = {}
            for subject in subjects:
                subject_dict[subject.name] = {}

                first_term = "First term"
                first_term_mark = get_term_data(first_term, session, stu, subject)

                second_term = "2nd Term"
                second_term_mark = get_term_data(second_term, session, stu, subject)

                third_term = "3rd Term"
                third_term_mark = get_term_data(third_term, session, stu, subject)

                first_final_mark = calc_mark_by_weightage(first_term, first_term_mark)
                second_final_mark = calc_mark_by_weightage(second_term, second_term_mark)
                third_final_mark = calc_mark_by_weightage(third_term, third_term_mark)
                all_term_total = first_final_mark + second_final_mark + third_final_mark

                subject_dict[subject.name]['first'] = first_final_mark
                subject_dict[subject.name]['second'] = second_final_mark
                subject_dict[subject.name]['third'] = third_final_mark
                subject_dict[subject.name]['all'] = all_term_total
                total += all_term_total
                real_total += 100

            bulk[student] = {
                "student": stu,
                "subjects": subject_dict,
                "percentage": str((total/real_total) * 100) + "%"
            }

        else:
            messages.warning(request, f"Result not generated for student {stu} as no class is assigned.")

        
    return bulk
