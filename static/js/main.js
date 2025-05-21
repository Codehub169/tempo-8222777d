document.addEventListener('DOMContentLoaded', function() {
    // --- Update current year in footer ---
    const yearSpan = document.getElementById('current-year');
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }

    // --- Index Page: Quiz Generation Form Validation ---
    const quizGenerationForm = document.querySelector('form[action*="/generate_quiz"]'); // Matches main_routes.py
    if (quizGenerationForm) {
        quizGenerationForm.addEventListener('submit', function(event) {
            const fileUpload = quizGenerationForm.querySelector('input[name="file_upload"]');
            const textInput = quizGenerationForm.querySelector('textarea[name="text_input"]');
            const numMcqInput = quizGenerationForm.querySelector('input[name="num_mcq"]');
            const numTfInput = quizGenerationForm.querySelector('input[name="num_tf"]');
            const numSaInput = quizGenerationForm.querySelector('input[name="num_sa"]');

            let errorMessages = [];

            // 1. Validate input source (file or text)
            if ((!fileUpload || !fileUpload.files || fileUpload.files.length === 0) && (!textInput || textInput.value.trim() === '')) {
                errorMessages.push('Please upload a file or paste text content.');
            }

            // 2. Validate question counts
            // Helper to parse counts, defaulting empty/invalid to 0 for sum, but preserving original for validation
            const getCount = (inputElement) => {
                if (!inputElement) return { value: '0', count: 0 }; // Element not found
                const valStr = inputElement.value;
                const count = parseInt(valStr, 10);
                return { value: valStr, count: isNaN(count) ? 0 : count, rawCount: count }; // rawCount can be NaN
            };

            const mcq = getCount(numMcqInput);
            const tf = getCount(numTfInput);
            const sa = getCount(numSaInput);

            if ((mcq.value !== "" && (isNaN(mcq.rawCount) || mcq.rawCount < 0)) ||
                (tf.value !== "" && (isNaN(tf.rawCount) || tf.rawCount < 0)) ||
                (sa.value !== "" && (isNaN(sa.rawCount) || sa.rawCount < 0))) {
                errorMessages.push('Please enter valid, non-negative numbers for question counts.');
            } else {
                const totalPositiveQuestions = 
                    (mcq.count < 0 ? 0 : mcq.count) + 
                    (tf.count < 0 ? 0 : tf.count) + 
                    (sa.count < 0 ? 0 : sa.count);

                if (totalPositiveQuestions === 0 && errorMessages.length === 0) { // Only add if no other count error
                    errorMessages.push('Please request at least one question by setting a count greater than 0 for at least one question type.');
                }
            }

            if (errorMessages.length > 0) {
                event.preventDefault(); // Prevent form submission
                // Consider a more user-friendly way to display errors than multiple alerts or one long alert.
                alert(errorMessages.join('\n')); 
            }
        });
    }

    // --- Quiz View Page: Toggle Submit Answer Button State ---
    const quizForm = document.getElementById('quiz-form'); // Form ID from quiz_view.html
    if (quizForm) {
        const submitAnswerButton = quizForm.querySelector('button[name="submit_answer_button"]'); 
        
        if (submitAnswerButton) { 
            const answerInputs = quizForm.querySelectorAll('input[type="radio"][name="answer"], textarea[name="answer"]');

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
                input.addEventListener('input', toggleSubmitButtonState); // 'input' works for radio changes too and textareas
            });
            toggleSubmitButtonState(); // Initial state check
        }
    }

    // --- Mobile Navigation Toggle (placeholder) ---
    // const navToggle = document.querySelector('.navbar-toggle');
    // const navMenu = document.querySelector('.nav-links'); // Ensure this class matches HTML
    // if (navToggle && navMenu) {
    //     navToggle.addEventListener('click', function() {
    //         navMenu.classList.toggle('active'); 
    //     });
    // }
});
