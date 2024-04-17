from flask import Flask, render_template, request, session, redirect, url_for
import json
from typing import Dict, Any

app = Flask(__name__)


data_cache: Dict[str, Any] = {}

def load_data() -> Dict[str, Any]:
    global data_cache
    if not data_cache:
        try:
            with open('data.json', 'r') as file:
                data_cache = json.load(file)
        except FileNotFoundError:
            print("The data file was not found.")
            raise
    return data_cache

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/learn/<int:lesson_id>')
def learn(lesson_id: int):
    data = load_data()
    lesson = next((l for l in data.get('lessons', []) if l['id'] == lesson_id), None)
    if lesson:
        return render_template('learn.html', lesson=lesson, total_lessons=len(data['lessons']))
    else:
        return render_template('error.html', error="Lesson not found"), 404

@app.route('/quiz/question/<int:question_number>')
def quiz_question(question_number: int):
    """Serve a specific quiz question by number."""
    questions = load_data().get('quiz', [])
    if question_number < 1 or question_number > len(questions):
        return render_template('error.html', error="Question not found"), 404
    question = questions[question_number - 1]  # Adjust for zero-based index
    return render_template('question.html', question=question, question_number=question_number, total_questions=len(questions))

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Process a single answer submission and redirect to the next question or the results page."""
    question_number = int(request.form['question_number'])
    selected_answer = request.form['selected_answer']
    # Collect all answers provided so far
    answers = {key: value for key, value in request.form.items() if key.startswith('answer_')}
    # Store the user's current answer
    answers[f'answer_{question_number}'] = selected_answer
    
    # Load questions
    questions = load_data().get('quiz', [])
    
    if question_number >= len(questions):
        # If it's the last question, calculate the score and show results
        score = sum(answers.get(f'answer_{i+1}') == questions[i]['correct_answer'] for i in range(len(questions)))
        # Render the results template with the user's score
        return render_template('results.html', score=score, total_questions=len(questions))
    else:
        # If there are more questions, redirect to the next one
        next_question_number = question_number + 1
        # Include the current state of answers as query parameters for the next question
        query_params = '&'.join([f'answer_{i}={answers[f"answer_{i}"]}' for i in range(1, question_number + 1)])
        return redirect(url_for('quiz_question', question_number=next_question_number) + f'?{query_params}')


if __name__ == '__main__':
    app.run(debug=True)
