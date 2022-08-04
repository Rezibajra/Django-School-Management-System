from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth import get_user_model

from .models import Staff

class StaffListView(ListView):
    model = Staff

class StaffDetailView(DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"


class StaffCreateView(SuccessMessageMixin, CreateView):
    model = Staff
    fields = "__all__"
    success_message = "New staff successfully added"
    def get_form(self):
        """add date picker in forms"""
        form = super(StaffCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})

        #Added
        # if form.is_valid():
        #     User = get_user_model()
        #     username = f"{form.cleaned_data['surname']} {form.cleaned_data['firstname']} {form.cleaned_data['other_name']}"
        #     default_password = create_default_password(username)
        #     user = User.objects.create_user(username = username, password = default_password, member_id = 1)
        #     user.save()
        return form


class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        print(self.kwargs['pk'])
        # if form.is_valid():
        #     username = f"{form.cleaned_data['surname']} {form.cleaned_data['firstname']} {form.cleaned_data['other_name']}"
        #     User.objects.update_or_create(username=username)
        return form


# class StaffDeleteView(DeleteView):
#     model = Staff
#     # print(Staff.objects.values())
#     # User.objects.filter(username = Staff.objects.values()[0]['firstname']).delete()
#     # success_url = reverse_lazy("staff-list")

#Added
def delete_staff(request, pk):
    User = get_user_model()
    staff = Staff.objects.get(id = pk)

    if request.method == 'POST':
        staff.delete()
        User.objects.filter(username=staff).delete()
        return redirect("staff-list")

    context = {'staff':staff}
    return render(request, "staffs/staff_confirm_delete.html", context)


