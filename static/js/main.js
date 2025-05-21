document.addEventListener('DOMContentLoaded', function() {
    // --- Index Page: Quiz Generation Form Validation ---
    const quizGenerationForm = document.querySelector('form[action*="/generate_quiz"]');
    if (quizGenerationForm) {
        quizGenerationForm.addEventListener('submit', function(event) {
            const fileUpload = quizGenerationForm.querySelector('input[name="file_upload"]');
            const textInput = quizGenerationForm.querySelector('textarea[name="text_input"]');
            const numMcqInput = quizGenerationForm.querySelector('input[name="num_mcq"]');
            const numTfInput = quizGenerationForm.querySelector('input[name="num_tf"]');
            const numSaInput = quizGenerationForm.querySelector('input[name="num_sa"]');

            let errorMessages = [];

            // 1. Validate input source (file or text)
            if ((!fileUpload || !fileUpload.files || !fileUpload.files[0]) && (!textInput || textInput.value.trim() === '')) {
                errorMessages.push('Please upload a file or paste text content.');
            }

            // 2. Validate question counts
            const numMcqVal = numMcqInput ? numMcqInput.value : '0'; // Default to '0' string if input element is missing, else actual value (can be "")
            const numTfVal = numTfInput ? numTfInput.value : '0';
            const numSaVal = numSaInput ? numSaInput.value : '0';

            const mcqCount = parseInt(numMcqVal, 10); // NaN if numMcqVal is "", 0 if numMcqVal is "0"
            const tfCount = parseInt(numTfVal, 10);
            const saCount = parseInt(numSaVal, 10);

            // Check if any field that is NOT an empty string resulted in NaN OR is negative
            if ((numMcqVal !== "" && (isNaN(mcqCount) || mcqCount < 0)) ||
                (numTfVal !== "" && (isNaN(tfCount) || tfCount < 0)) ||
                (numSaVal !== "" && (isNaN(saCount) || saCount < 0))) {
                errorMessages.push('Please enter valid, non-negative numbers for question counts.');
            } else {
                // All fields are either empty, or represent valid non-negative numbers (or were missing and defaulted to '0')
                // Now check total. NaN (from empty field) will be treated as 0 by the sum logic.
                const totalPositiveQuestions = 
                    (isNaN(mcqCount) || mcqCount < 0 ? 0 : mcqCount) +
                    (isNaN(tfCount) || tfCount < 0 ? 0 : tfCount) +
                    (isNaN(saCount) || saCount < 0 ? 0 : saCount);

                if (totalPositiveQuestions === 0) {
                    errorMessages.push('Please request at least one question by setting a count greater than 0 for at least one question type.');
                }
            }

            if (errorMessages.length > 0) {
                event.preventDefault(); // Prevent form submission
                alert(errorMessages.join('\n'));
            }
        });
    }

    // --- Quiz View Page: Toggle Submit Answer Button State ---
    const quizForm = document.getElementById('quiz-form'); // Form ID from quiz_view.html
    if (quizForm) {
        const submitAnswerButton = quizForm.querySelector('button[name="submit_answer_btn"]'); 
        
        if (submitAnswerButton) { // Only proceed if the button is on the page
            const answerInputs = quizForm.querySelectorAll('input[type="radio"], textarea[name="short_answer_text"]');

            const toggleSubmitButtonState = () => {
                let anAnswerIsProvided = false;
                answerInputs.forEach(input => {
                    if (input.type === 'radio' && input.checked) {
                        anAnswerIsProvided = true;
                    }
                    if (input.tagName === 'TEXTAREA' && input.value.trim() !== '') {
                        anAnswerIsProvided = true;
                    }
                });
                submitAnswerButton.disabled = !anAnswerIsProvided;
            };

            answerInputs.forEach(input => {
                if (input.type === 'radio') {
                    input.addEventListener('change', toggleSubmitButtonState);
                }
                if (input.tagName === 'TEXTAREA') {
                    input.addEventListener('input', toggleSubmitButtonState);
                }
            });

            // Initial state check on page load
            toggleSubmitButtonState();
        }
    }

    // --- Mobile Navigation Toggle (if a .navbar-toggle button and .navbar-links exists) ---
    const navToggle = document.querySelector('.navbar-toggle');
    const navMenu = document.querySelector('.navbar-links'); 

    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active'); 
        });
    }
});
