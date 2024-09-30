from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from llm_guard.input_scanners import BanTopics, PromptInjection, Toxicity, TokenLimit, Language
from llm_guard.input_scanners.language import MatchType
from llm_guard.output_scanners import NoRefusal, Relevance, Sensitive
from llm_guard import scan_prompt
from llm_guard import scan_output

# Initialize the topic scanner from llm-guard
# Have different BanTopics with different thresholds
input_scanners = [
    Toxicity(),
    PromptInjection(),
    TokenLimit(limit=1024),
    Language(valid_languages=["en"], match_type=MatchType.FULL),
    BanTopics(topics=["suicide"], threshold=0.5),
    BanTopics(topics=["violence"], threshold=0.6),
    BanTopics(topics=["bullying"], threshold=0.6),
]

output_scanners = [
    Language(valid_languages=["en"], match_type=MatchType.FULL),
    Relevance(),
    Sensitive()
]

template = """
Answer the question below regarding mental health support.

Here is the question: {question}

Answer: 
"""

# Using the dolphin-phi uncensored model
model = OllamaLLM(model="dolphin-phi")
# Prompt template
prompt = ChatPromptTemplate.from_template(template)
# Create a langchain between the prompt and the model
chain = prompt | model

# Start of the flask application
app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# API for prompting the AI model on generic mental health support questions
@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_input = data.get("user_input")

    # Scan the user's input with input scanners
    sanitized_prompt, results_valid, results_score = scan_prompt(
        input_scanners, user_input, fail_fast=True)

    # Return error if do not pass input scanners
    if any(not result for result in results_valid.values()):
        return jsonify({"status": "ERROR", "response": "Your input contains prohibited topics.", "risk_score": results_score}), 200

    # Generate response using the user input
    result = chain.invoke({"question": user_input})
    response = str(result)

    # Scan the response with output scanners
    sanitized_response_text, results_valid, results_score = scan_output(
        output_scanners, sanitized_prompt, response
    )

    # Return error if do not pass output scanners
    if any(not result for result in results_valid.values()):
        return jsonify({"status": "ERROR", "response": "The output contains prohibited topics.", "risk_score": results_score}), 200

    return jsonify({"status": "OK", "response": response})

# API for when user wants to check what are the emergency resources for mental health help
@app.route("/emergency-resources", methods=["GET"])
def emergencyResources():
    try:
        # Attempt a simple model query to check what are the available emergency resources
        result = chain.invoke(
            {"question": "What are the emergency resources I can reach out to in Singapore, for mental health support?"})
        if result:
            return jsonify({"status": "OK", "message": "Model is running.", "response": str(result)})
        else:
            return jsonify({"status": "ERROR", "message": "Model response is empty."}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500

# API for when user wants to check the status of the AI model
@app.route("/status", methods=["GET"])
def status():
    try:
        result = model.invoke(input="Check if the AI model is functioning.")
        if result:
            return jsonify({"status": "OK", "message": "Model is running.", "response": str(result)})
        else:
            return jsonify({"status": "ERROR", "message": "Model response is empty."}), 500
    except Exception as e:
        return jsonify({"status": "ERROR", "message": str(e)}), 500


if __name__ == "__main__":
    app.run()
