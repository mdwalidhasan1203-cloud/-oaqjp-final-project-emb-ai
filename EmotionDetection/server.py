"""
server.py

Flask web application that provides a simple interface for the emotion
detection service. Users submit text, and the app displays the detected
emotion scores and the dominant emotion.
"""

from flask import Flask, render_template, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/")
def render_index_page():
    """Render the main input page."""
    return render_template('index.html')


@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Handle a request to analyze text submitted via query parameter
    'textToAnalyze'. Returns a formatted string describing the detected
    emotions and the dominant emotion, or an error message for blank or
    invalid input.
    """
    text_to_analyze = request.args.get('textToAnalyze', '')

    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    result = emotion_detector(text_to_analyze)

    if result['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    response_text = (
        f"For the given statement, the system response is "
        f"'anger': {result['anger']}, "
        f"'disgust': {result['disgust']}, "
        f"'fear': {result['fear']}, "
        f"'joy': {result['joy']} and "
        f"'sadness': {result['sadness']}. "
        f"The dominant emotion is {result['dominant_emotion']}."
    )
    return response_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
