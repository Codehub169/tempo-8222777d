import google.generativeai as genai
import os
from flask import current_app
import json

ALLOWED_QUESTION_TYPES = ["MCQ", "True/False", "Short Answer"]

def configure_gemini():
    """Configures the Gemini API with the API key from Flask app config."""
    api_key = current_app.config.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in configuration.")
    genai.configure(api_key=api_key)

def generate_quiz_from_text(text_content, num_mcq=5, num_tf=3, num_sa=2, topic="general"):
    """Generates a quiz from the given text content using Gemini API.

    Args:
        text_content (str): The educational content to analyze.
        num_mcq (int): Number of Multiple Choice Questions to generate.
        num_tf (int): Number of True/False Questions to generate.
        num_sa (int): Number of Short Answer Questions to generate.
        topic (str): Optional topic to guide quiz generation.

    Returns:
        list: A list of question dictionaries, or None if an error occurs.
              Each dictionary should have 'type', 'text', 'options' (for MCQ),
              'correct_answer', 'explanation'.
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-pro') # Or other suitable model

        prompt = f"""Analyze the following educational content on the topic of '{topic}'. 
        Based *only* on the information present in this content, generate a quiz with the following structure:
        1. {num_mcq} Multiple Choice Questions (MCQs). For each MCQ, provide 4 options, clearly indicate the correct answer, and provide a brief explanation for why it's correct.
        2. {num_tf} True/False questions. For each, state the correct answer (True or False) and a brief explanation.
        3. {num_sa} Short Answer questions. For each, provide an ideal short answer and a brief explanation of what key points the answer should cover.

        Format the output as a JSON array of question objects. Each object must have:
        - "type": string (must be one of {', '.join(ALLOWED_QUESTION_TYPES)})
        - "text": string (the question itself)
        - "options": array of strings (for MCQ only, 4 options)
        - "correct_answer": string (for MCQ, the text of the correct option; for TF, "True" or "False"; for SA, the ideal answer)
        - "explanation": string (brief explanation for the answer)

        Content:
        ---BEGIN CONTENT---
        {text_content}
        ---END CONTENT---

        JSON Output:
        """

        response = model.generate_content(prompt)
        
        # Debugging: Print raw response text
        # print("Gemini Raw Response Text:", response.text)

        # Attempt to parse the JSON response
        # The API might return text that needs to be cleaned (e.g., ```json ... ``` wrappers)
        cleaned_response_text = response.text.strip()
        if cleaned_response_text.startswith("```json"):
            cleaned_response_text = cleaned_response_text[7:]
        if cleaned_response_text.endswith("```"):
            cleaned_response_text = cleaned_response_text[:-3]
        
        quiz_data = json.loads(cleaned_response_text.strip())
        
        # Validate structure (basic validation)
        if not isinstance(quiz_data, list):
            raise ValueError("Generated quiz data is not a list.")
        for q_data in quiz_data:
            if not all(key in q_data for key in ['type', 'text', 'correct_answer', 'explanation']):
                raise ValueError("Missing required keys in question data.")
            if q_data['type'] == "MCQ" and (not 'options' in q_data or not isinstance(q_data['options'], list) or len(q_data['options']) != 4):
                 raise ValueError("MCQ missing options or incorrect number of options.")
            if q_data['type'] not in ALLOWED_QUESTION_TYPES:
                raise ValueError(f"Invalid question type: {q_data['type']}")

        return quiz_data

    except Exception as e:
        current_app.logger.error(f"Error generating quiz with Gemini: {e}")
        current_app.logger.error(f"Gemini prompt used: {prompt}")
        if 'response' in locals() and hasattr(response, 'text'):
             current_app.logger.error(f"Gemini raw response: {response.text}")
        return None
