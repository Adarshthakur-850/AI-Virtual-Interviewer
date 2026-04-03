import json
from src.prompts import SYSTEM_PROMPT_GENERATOR, SYSTEM_PROMPT_EVALUATOR

def generate_questions(client, role, count=5):
    """Generates interview questions using OpenAI API."""
    try:
        prompt = SYSTEM_PROMPT_GENERATOR.format(role=role, count=count)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7
        )
        content = response.choices[0].message.content.strip()
        # Ensure clean JSON parsing
        if "```json" in content:
            content = content.replace("```json", "").replace("```", "")
        questions = json.loads(content)
        return questions
    except Exception as e:
        print(f"Error generating questions: {e}")
        # Fallback questions if API fails
        return [
            f"Explain the core concepts of {role}.",
            "Describe a challenging project you worked on.",
            "How do you handle debugging in complex systems?",
            "What is your preferred tech stack and why?",
            "Explain how you would optimize a slow system."
        ]

def evaluate_answer(client, role, question, answer):
    """Evaluates a single answer using OpenAI API."""
    if not answer or len(answer.strip()) < 5:
        return {
            "score": 0, 
            "feedback": "Answer too short or empty.",
            "strengths": [],
            "improvements": ["Provide a detailed explanation."]
        }

    try:
        prompt = SYSTEM_PROMPT_EVALUATOR.format(role=role, question=question, answer=answer)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        if "```json" in content:
            content = content.replace("```json", "").replace("```", "")
        evaluation = json.loads(content)
        return evaluation
    except Exception as e:
        print(f"Error evaluating answer: {e}")
        return {
            "score": 5,
            "feedback": "Could not generate detailed AI feedback due to an error.",
            "strengths": ["N/A"],
            "improvements": ["N/A"]
        }
