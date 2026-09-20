# Emotion Detection Application

This repository contains the Final Project for the Emotion Detector course.

An emotion detection application that analyzes text using the Watson NLP
EmotionPredict service, packaged as a Python module with a Flask web
front end.

## Project Structure

```
EmotionDetection/
├── EmotionDetection/
│   ├── __init__.py
│   └── emotion_detection.py
├── templates/
│   └── index.html
├── server.py
├── test_emotion_detection.py
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the tests

```bash
python -m unittest test_emotion_detection.py
```

## Running the web app

```bash
python server.py
```

Then open `http://localhost:5000` in a browser, type some text, and click
**Analyze** to see the detected emotion scores and dominant emotion.

## Static code analysis

```bash
pylint EmotionDetection/emotion_detection.py server.py EmotionDetection/__init__.py test_emotion_detection.py
```

The codebase is currently rated 10.00/10 (aside from the unavoidable
`invalid-name` notice on the `EmotionDetection` package directory itself,
whose name is fixed by the project spec).

## How it works

1. The user enters text in the web form (`templates/index.html`).
2. The browser sends a GET request to `/emotionDetector?textToAnalyze=...`.
3. `server.py` calls `emotion_detector()` from the `EmotionDetection` package.
4. `emotion_detector()` posts the text to the Watson NLP EmotionPredict
   endpoint, parses the response, and returns a dictionary of scores for
   `anger`, `disgust`, `fear`, `joy`, and `sadness`, plus the
   `dominant_emotion` (the highest-scoring one).
5. `server.py` formats this into a readable sentence and returns it to the
   page, which displays it to the user.

## Error handling

* **Blank input:** `emotion_detector()` returns `None` for every value
  without calling the service; `server.py` shows
  `"Invalid text! Please try again!"` and the page's JavaScript also
  catches empty submissions client-side with `"Please enter some text."`.
* **Service errors (HTTP 400 or other non-200 responses):** caught and
  turned into the same `None`-filled result rather than letting the
  application crash, so `server.py` can show a friendly error message.
* **Network failures:** wrapped in a `try/except` around the `requests`
  call so a timeout or connection error doesn't crash the app either.

## Note on the Watson NLP endpoint

This app calls the Watson NLP `EmotionPredict` service at
`sn-watson-emotion.labs.skills.network` — the standard endpoint used for
this exercise (e.g. via IBM Skills Network labs, which provision it for
you). If you're running this outside that environment, you'll need
access to an equivalent Watson NLP emotion-detection deployment, and
should update the `url` in `EmotionDetection/emotion_detection.py`
accordingly.
