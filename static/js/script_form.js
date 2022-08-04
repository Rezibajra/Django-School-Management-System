
(() => {
    let formControl1 = document.querySelector("#id_subject");
    let exam_score1 = document.querySelector("#id_exam_score");
    let test_score1 = document.querySelector("#id_test_score");
    let performance_score1 = document.querySelector("#id_performance_score");
    let listening_score1 = document.querySelector("#id_listening_score");
    let speaking_score1 = document.querySelector("#id_speaking_score");
    let btn = document.querySelectorAll(".btn");

    let selected_subject = formControl1.options[formControl1.options.selectedIndex].innerHTML.toLowerCase();

    let exam_input_score = parseInt(exam_score1.options[exam_score1.options.selectedIndex].textContent);
    let test_input_score = parseInt(test_score1.options[test_score1.options.selectedIndex].textContent);
    let performance_input_score = parseInt(performance_score1.options[performance_score1.options.selectedIndex].textContent);
    let listening_input_score = 0;
    let speaking_input_score = 0;

    if (selected_subject == 'english') {
        listening_input_score = parseInt(listening_score1.options[listening_score1.options.selectedIndex].textContent);
        speaking_input_score = parseInt(speaking_score1.options[speaking_score1.options.selectedIndex].textContent);
    }

    exam_score1.addEventListener('change', (e) => {
        exam_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
        exam_input_score = nanCheckSet(exam_input_score);
        if (test_input_score != '' || exam_input_score != '' || performance_input_score != '') {
            marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
        }
    });
    test_score1.addEventListener('change', (e) => {
        test_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
        test_input_score = nanCheckSet(test_input_score);
        if (test_input_score != '' || exam_input_score != '' || performance_input_score != '') {
            marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
        }
    });
    performance_score1.addEventListener('change', (e) => {
        performance_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
        performance_input_score = nanCheckSet(performance_input_score);
        if (performance_input_score != '' || test_input_score != '' || exam_input_score != '') {
            marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
        }
    });
    if (selected_subject == 'english') {
        listening_score1.addEventListener('change', (e) => {
            listening_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
            listening_input_score = nanCheckSet(listening_input_score);
            if (performance_input_score != '' || test_input_score != '' || exam_input_score != '' || listening_input_score != '' || speaking_input_score != '') {
                marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
            }
        });
        speaking_score1.addEventListener('change', (e) => {
            speaking_input_score = parseInt(e.target.options[e.target.options.selectedIndex].textContent);
            speaking_input_score = nanCheckSet(speaking_input_score);
            if (performance_input_score != '' || test_input_score != '' || exam_input_score != '' || listening_input_score != '' || speaking_input_score != '') {
                marksSumCheck(exam_input_score, test_input_score, performance_input_score, listening_input_score, speaking_input_score);
            }
        });
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
            exam_score1.classList.remove("is-invalid");
            test_score1.classList.remove("is-invalid");
            performance_score1.classList.remove("is-invalid");
            if (selected_subject == 'english') {
                listening_score1.classList.remove("is-invalid");
                speaking_score1.classList.remove("is-invalid");
            }
            error.textContent = ""
            btn[0].disabled = false;
        } else {
            exam_score1.classList.add("is-invalid");
            test_score1.classList.add("is-invalid");
            performance_score1.classList.add("is-invalid");
            if (selected_subject == 'english') {
                listening_score1.classList.add("is-invalid");
                speaking_score1.classList.add("is-invalid");
            }
            error.textContent = "The marks allocation has exceeded 100%."
            error.style.color = "red";
            error.style.margin = "auto"
            error.style.display = "table";
            btn[0].disabled = true;
        }   
    }
})();