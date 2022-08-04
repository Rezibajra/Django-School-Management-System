
(()=>{
    let formControl = document.querySelector("#id_Mark-subject");
    let exam_score = document.querySelector("#id_Mark-exam_score");
    let test_score = document.querySelector("#id_Mark-test_score");
    let performance_score = document.querySelector("#id_Mark-performance_score");
    let listening_score = document.querySelector("#id_Mark-listening_score");
    let speaking_score = document.querySelector("#id_Mark-speaking_score");
    let labels = document.getElementsByTagName("label");
    let btn = document.querySelectorAll(".btn");
    let error = document.getElementById("error");
    let selected_subject = "";

    let exam_input_score = 0;
    let test_input_score = 0;
    let performance_input_score = 0;
    let listening_input_score = 0;
    let speaking_input_score = 0;

    formControl.addEventListener('change', (e) => dynamicOptionDisplay(e));

    const dynamicOptionDisplay = (e) => {

        clearFields();

        let selected_id = e.target.options.selectedIndex;
        selected_subject = e.target.options[selected_id].innerHTML.toLowerCase();

        if (selected_subject != 'english') {
            listening_score.style.display = "none";
            speaking_score.style.display = "none";
            localStorage.setItem('show', 'false');
        } else {
            listening_score.style.display = "block";
            speaking_score.style.display = "block";
            localStorage.setItem('show', 'true');
        }
        dynamicLabelDisplay(selected_subject);
        marksRetrieve(e);
    }

    const clearFields = () => {
        exam_input_score = 0;
        test_input_score = 0;
        performance_input_score = 0;
        listening_input_score = 0;
        speaking_input_score = 0;
        exam_score.options.selectedIndex = 0;
        test_score.options.selectedIndex = 0;
        performance_score.options.selectedIndex = 0;
        listening_score.options.selectedIndex = 0;
        speaking_score.options.selectedIndex = 0;
        exam_score.classList.remove("is-invalid");
        test_score.classList.remove("is-invalid");
        performance_score.classList.remove("is-invalid");
        listening_score.classList.remove("is-invalid");
        speaking_score.classList.remove("is-invalid");
        error.textContent = ""
    }

    const dynamicLabelDisplay = (subject) => {
        for (let label of labels) {
            let label_id = label.htmlFor;
            if (subject != 'english') {
                if (label_id == 'id_Mark-listening_score' || label_id == 'id_Mark-speaking_score') {
                    label.hidden = true;
                }
            } else {
                label.hidden = false;
            }
        }
    }


    const marksRetrieve = () => {
        exam_score.addEventListener('change', (e) => {
            exam_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
            exam_input_score = nanCheckSet(exam_input_score);
            if (test_input_score != '' || exam_input_score != '' || performance_input_score != '') {
                marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
            }
        });
        test_score.addEventListener('change', (e) => {
            test_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
            test_input_score = nanCheckSet(test_input_score);
            if (test_input_score != '' || exam_input_score != '' || performance_input_score != '') {
                marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
            }
        });
        performance_score.addEventListener('change', (e) => {
            performance_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
            performance_input_score = nanCheckSet(performance_input_score);
            if (performance_input_score != '' || test_input_score != '' || exam_input_score != '') {
                marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
            }
        });
        if (selected_subject == 'english') {
            listening_score.addEventListener('change', (e) => {
                listening_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
                listening_input_score = nanCheckSet(listening_input_score);
                if (performance_input_score != '' || test_input_score != '' || exam_input_score != '' || listening_input_score != '' || speaking_input_score != '') {
                    marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
                }
            });
            speaking_score.addEventListener('change', (e) => {
                speaking_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
                speaking_input_score = nanCheckSet(speaking_input_score);
                if (performance_input_score != '' || test_input_score != '' || exam_input_score != '' || listening_input_score != '' || speaking_input_score != '') {
                    marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
                }
            });
        }
    }

    const nanCheckSet = (input_score) => {
        if (isNaN(input_score)) {
            input_score = 0;
            return input_score;
        } else {
            return input_score;
        }
    }


    const marksSumCheck = (exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score) => {
        let sum_total = 0;
        sum_total = exam_input_score + test_input_score + performance_input_score + listening_input_score + speaking_input_score;
        console.log("hello", sum_total);
        
        if (sum_total <= 100 || isNaN(sum_total)) {
            exam_score.classList.remove("is-invalid");
            test_score.classList.remove("is-invalid");
            performance_score.classList.remove("is-invalid");
            if (selected_subject == 'english') {
                listening_score.classList.remove("is-invalid");
                speaking_score.classList.remove("is-invalid");
            }
            error.textContent = ""
            btn[2].disabled = false;
        } else {
            exam_score.classList.add("is-invalid");
            test_score.classList.add("is-invalid");
            performance_score.classList.add("is-invalid");
            if (selected_subject == 'english') {
                listening_score.classList.add("is-invalid");
                speaking_score.classList.add("is-invalid");
            }
            error.textContent = "The marks allocation has exceeded 100%."
            error.style.color = "red";
            error.style.margin = "auto"
            error.style.display = "table";
            btn[2].disabled = true;
        }   
    }

    //clear modal data on close.
    $(document).ready(function(){
        $("#modal1").on('hidden.bs.modal', function(){
            $('#modal1 form')[0].reset();
            error.textContent = "";
            exam_score.classList.remove("is-invalid");
            test_score.classList.remove("is-invalid");
            performance_score.classList.remove("is-invalid");
            listening_score.classList.remove("is-invalid");
            speaking_score.classList.remove("is-invalid");
        });
    });


    window.onload = () => {
        let show = localStorage.getItem('show');
        loadOptionChanging(show)
    }

    const loadOptionChanging = (show) => {
        if (show == 'true' || selected_subject == 'english'){
            listening_score.style.display = "block";
            speaking_score.style.display = "block";
            setLabelVisibility(false);
        } else {
            listening_score.style.display = "none";
            speaking_score.style.display = "none";
            setLabelVisibility(true);
        }
    }

    const setLabelVisibility = (boolValue) => {
        for (let label of labels) {
            let label_id = label.htmlFor;
            if (label_id == 'id_Mark-listening_score' || label_id == 'id_Mark-speaking_score') {
                label.hidden = boolValue;
            }
        }
    }
})();
