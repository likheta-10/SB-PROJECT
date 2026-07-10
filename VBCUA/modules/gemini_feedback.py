import google.generativeai as genai

# ----------------------------------------
# Enter Your Gemini API Key
# ----------------------------------------

genai.configure(api_key="AQ.Ab8RN6Lmiyhxsx2j7A-JtA_F6tCmT4KcA8xcRsrEN_vz0LJyDA")

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_feedback(
        concept,
        transcript,
        semantic_score,
        filler_count,
        pause_ratio):

    prompt = f"""
You are an AI Communication and Concept Evaluation Assistant.

Evaluate the following spoken explanation.

Concept:
{concept}

Transcript:
{transcript}

Semantic Score:
{semantic_score:.2f}

Filler Words:
{filler_count}

Pause Ratio:
{pause_ratio}

Generate a report with exactly these headings:

Understanding Level

Strengths

Weaknesses

Suggestions for Improvement

Overall Feedback

Keep the response under 200 words.
"""

    response = model.generate_content(prompt)

    return response.text