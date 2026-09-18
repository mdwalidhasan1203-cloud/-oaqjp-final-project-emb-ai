"""
emotion_detection.py

This module provides the emotion_detector function, which sends text to the
Watson NLP EmotionPredict service and returns a structured dictionary of
emotion scores along with the dominant emotion.
"""

import json
import requests


def emotion_detector(text_to_analyze):
    """
    Send text to the Watson NLP EmotionPredict service and return a
    dictionary of emotion scores plus the dominant emotion.

    Args:
        text_to_analyze (str): The text to run emotion detection on.

    Returns:
        dict: A dictionary with keys 'anger', 'disgust', 'fear', 'joy',
              'sadness', and 'dominant_emotion'. If the input is blank or
              the service returns an error (e.g. HTTP 400), every value in
              the dictionary is set to None.
    """
    url = (
        'https://sn-watson-emotion.labs.skills.network/v1/'
        'watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = {"raw_document": {"text": text_to_analyze}}

    blank_result = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None,
    }

    # Guard against blank/whitespace-only input before making a network call.
    if not text_to_analyze or not text_to_analyze.strip():
        return blank_result

    try:
        response = requests.post(url, json=input_json, headers=headers, timeout=10)
    except requests.exceptions.RequestException:
        # Network-level failure (timeout, connection error, etc.)
        return blank_result

    # Watson NLP returns 400 for malformed/blank input server-side too.
    if response.status_code == 400:
        return blank_result

    if response.status_code != 200:
        return blank_result

    try:
        raw = json.loads(response.text)
        emotions = raw['emotionPredictions'][0]['emotion']
    except (ValueError, KeyError, IndexError):
        return blank_result

    formatted = {
        'anger': emotions.get('anger'),
        'disgust': emotions.get('disgust'),
        'fear': emotions.get('fear'),
        'joy': emotions.get('joy'),
        'sadness': emotions.get('sadness'),
    }

    dominant_emotion = max(formatted, key=formatted.get)
    formatted['dominant_emotion'] = dominant_emotion

    return formatted
