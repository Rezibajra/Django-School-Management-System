
(() => {
        let term_name = document.getElementById("id_Academic Term-name");
        let first_weightage = document.getElementById("id_Academic Term-first_weightage");
        let second_weightage = document.getElementById("id_Academic Term-second_weightage");
        let third_weightage = document.getElementById("id_Academic Term-third_weightage");
        let labels = document.getElementsByTagName("label");
        let btn = document.querySelectorAll(".btn");
        let error = document.getElementById("error");

        let first_input_weightage = 0;
        let second_input_weightage = 0;
        let third_input_weightage = 0;

        let term_current = term_name.value;
        console.log(term_current);

        const clearFields = () => {
            first_input_weightage = 0;
            second_input_weightage = 0;
            third_input_weightage = 0;
            first_weightage.options.selectedIndex = 0;
            second_weightage.options.selectedIndex = 0;
            third_weightage.options.selectedIndex = 0;
            first_weightage.classList.remove("is-invalid");
            second_weightage.classList.remove("is-invalid");
            third_weightage.classList.remove("is-invalid");
            error.textContent = ""
        }

        const dynamicLabelDisplay = (term) => {
            
            for (let label of labels) {
                let label_id = label.htmlFor;
                if (term != 'Final Result' || term == "none") {
                    if (label_id == 'id_Academic Term-first_weightage' || label_id == 'id_Academic Term-second_weightage' || label_id == 'id_Academic Term-third_weightage') {
                        label.hidden = true;
                    }
                } else {
                    label.hidden = false;
                }
            }
        }

        if (term_current == "Final Result") {
            if (btn[2]){
                console.log(btn[2]);
                btn[2].disabled = true;
            }
            first_weightage.style.display = "block";
            second_weightage.style.display = "block";
            third_weightage.style.display = "block";
            dynamicLabelDisplay(term_current);
        } else {
            first_weightage.style.display = "none";
            second_weightage.style.display = "none";
            third_weightage.style.display = "none";
            first_weightage.required = false;
            second_weightage.required = false;
            third_weightage.required = false;
            dynamicLabelDisplay(term_current);
        }
    
        const hideUnhideWeightage = () => {
            
            term_name.addEventListener('change', (e) => { 
                let t_name = e.target.options[e.target.options.selectedIndex].textContent;
                if (t_name == "Final Result") {
                    first_weightage.style.display = "block";
                    second_weightage.style.display = "block";
                    third_weightage.style.display = "block";
                    if (btn[2]){
                        console.log(btn[2]);
                        btn[2].disabled = true;
                    } else {
                        btn[0].disabled = true;
                    }
                } else {
                    first_weightage.style.display = "none";
                    second_weightage.style.display = "none";
                    third_weightage.style.display = "none";
                    first_weightage.required = false;
                    second_weightage.required = false;
                    third_weightage.required = false;
                    error.textContent = "";
                    if (btn[2]){
                        btn[2].disabled = false;
                    } else {
                        btn[0].disabled = false;
                    }
                }
                dynamicLabelDisplay(t_name);
            }
            )
        }

        hideUnhideWeightage();

        const marksSumCheck = (first_input_weightage, second_input_weightage, third_input_weightage) => {
            let sum_total = 0;
            
            sum_total = first_input_weightage + second_input_weightage + third_input_weightage;
            
            if (sum_total == 100 || isNaN(sum_total)) {
                first_weightage.classList.remove("is-invalid");
                second_weightage.classList.remove("is-invalid");
                third_weightage.classList.remove("is-invalid");
                error.textContent = ""
                if (btn[2]){
                    btn[2].disabled = false;
                } else {
                    btn[0].disabled = false;
                }
            } else if (sum_total > 100){
                first_weightage.classList.add("is-invalid");
                second_weightage.classList.add("is-invalid");
                third_weightage.classList.add("is-invalid");
                error.textContent = "The weightage allocation has exceeded 100%."
                error.style.color = "red";
                error.style.margin = "auto"
                error.style.display = "table";
                if (btn[2]){
                    btn[2].disabled = true;
                } else {
                    btn[0].disabled = true;
                }
            }  else {
                first_weightage.classList.add("is-invalid");
                second_weightage.classList.add("is-invalid");
                third_weightage.classList.add("is-invalid");
                error.textContent = "The weightage allocation must be equal to 100%."
                error.style.color = "red";
                error.style.margin = "auto"
                error.style.display = "table";
                if (btn[2]){
                    btn[2].disabled = true;
                } else {
                    btn[0].disabled = true;
                }
            }
           
            if ((first_input_weightage == 0 || second_input_weightage == 0 || third_input_weightage == 0) || (isNaN(first_input_weightage)) || isNaN(second_input_weightage) || isNaN(third_input_weightage)){
                error.textContent = "Please input all the fields."
                first_weightage.classList.add("is-invalid");
                second_weightage.classList.add("is-invalid");
                third_weightage.classList.add("is-invalid");
                error.style.color = "red";
                error.style.margin = "auto"
                error.style.display = "table";
                if (btn[2]){
                    btn[2].disabled = true;
                } else {
                    btn[0].disabled = true;
                }
            }
        }

        const weightageRetreive = () => {
            first_weightage.addEventListener('change', (e) => {
                first_input_weightage = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
                if (first_input_weightage != '' || second_input_weightage != '' || third_input_weightage != '') {
                    marksSumCheck(first_input_weightage, second_input_weightage, third_input_weightage);
                }
            });
            second_weightage.addEventListener('change', (e) => {
                second_input_weightage = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
                if (first_input_weightage != '' || second_input_weightage != '' || third_input_weightage != '') {
                    marksSumCheck(first_input_weightage, second_input_weightage, third_input_weightage);
                }
            });
            third_weightage.addEventListener('change', (e) => {
                third_input_weightage = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
                if (first_input_weightage != '' || second_input_weightage != '' || third_input_weightage != '') {
                    marksSumCheck(first_input_weightage, second_input_weightage, third_input_weightage);
                }
            });
        }

        weightageRetreive();

        $(document).ready(function(){
            $("#modal1").on('hidden.bs.modal', function(){
                $('#modal1 form')[0].reset();
                clearFields();
                error.textContent = "";
                first_weightage.classList.remove("is-invalid");
                second_weightage.classList.remove("is-invalid");
                third_weightage.classList.remove("is-invalid");
            });
        });

})();