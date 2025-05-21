from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

def generate_quiz_pdf(quiz_title, questions, output_dir, filename="quiz.pdf"):
    """
    Generates a PDF document for a given quiz.

    Args:
        quiz_title (str): The title of the quiz.
        questions (list): A list of question dictionaries. Each dictionary should have:
                          'type' (str: 'MCQ', 'TF', 'SA'),
                          'text' (str: question text),
                          'options' (list of str, for MCQ only),
                          'correct_answer' (str),
                          'explanation' (str, optional).
        output_dir (str): The directory to save the PDF file.
        filename (str): The name of the PDF file to generate.

    Returns:
        str: The full path to the generated PDF file, or None if generation failed.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filepath = os.path.join(output_dir, filename)
    doc = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'QuizTitle',
        parent=styles['h1'],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=0.5*inch
    )
    question_style = ParagraphStyle(
        'QuestionText',
        parent=styles['Normal'],
        fontSize=12,
        spaceBefore=0.2*inch,
        spaceAfter=0.1*inch,
        leading=14
    )
    option_style = ParagraphStyle(
        'OptionText',
        parent=styles['Normal'],
        fontSize=11,
        leftIndent=0.25*inch,
        leading=14
    )
    answer_style = ParagraphStyle(
        'AnswerText',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2c8431'), # Dark green
        spaceBefore=0.05*inch,
        leading=14
    )
    explanation_style = ParagraphStyle(
        'ExplanationText',
        parent=styles['Italic'],
        fontSize=10,
        textColor=colors.grey,
        leftIndent=0.1*inch,
        spaceAfter=0.2*inch,
        leading=12
    )

    story = []

    # Add Quiz Title
    story.append(Paragraph(quiz_title, title_style))

    for i, q_data in enumerate(questions):
        # Question Number and Text
        story.append(Paragraph(f"<b>Question {i+1}:</b> {q_data['text']}", question_style))

        # Options (for MCQ)
        if q_data['type'] == 'MCQ' and 'options' in q_data and q_data['options']:
            for opt_idx, option_text in enumerate(q_data['options']):
                option_label = chr(ord('A') + opt_idx) # A, B, C, D
                story.append(Paragraph(f"{option_label}. {option_text}", option_style))
        
        story.append(Spacer(1, 0.1*inch))

        # Correct Answer
        story.append(Paragraph(f"<b>Correct Answer:</b> {q_data['correct_answer']}", answer_style))

        # Explanation
        if q_data.get('explanation'):
            story.append(Paragraph(f"<i>Explanation:</i> {q_data['explanation']}", explanation_style))
        
        story.append(Spacer(1, 0.25*inch))
        # Add a page break if nearing the end of a page, to avoid awkward splits (optional)
        # This is a simple heuristic, ReportLab has more sophisticated ways for page layout.
        if (i+1) % 4 == 0 and i+1 < len(questions): # Roughly 4 questions per page
            pass # story.append(PageBreak()) 

    try:
        doc.build(story)
        return filepath
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

if __name__ == '__main__':
    # Example Usage (for testing purposes)
    sample_questions = [
        {
            "type": "MCQ",
            "text": "What is the powerhouse of the cell?",
            "options": ["Nucleus", "Ribosome", "Mitochondria", "Golgi Apparatus"],
            "correct_answer": "Mitochondria",
            "explanation": "Mitochondria are responsible for generating most of the cell's supply of adenosine triphosphate (ATP), used as a source of chemical energy."
        },
        {
            "type": "TF",
            "text": "The Earth is flat.",
            "correct_answer": "False",
            "explanation": "The Earth is an oblate spheroid."
        },
        {
            "type": "SA",
            "text": "What element has the chemical symbol 'O'?",
            "correct_answer": "Oxygen",
            "explanation": "'O' is the chemical symbol for Oxygen, which has an atomic number of 8."
        }
    ]
    pdf_path = generate_quiz_pdf("Sample Science Quiz", sample_questions, "./output_pdfs", "science_quiz.pdf")
    if pdf_path:
        print(f"Sample PDF generated at: {pdf_path}")
    else:
        print("Failed to generate sample PDF.")
