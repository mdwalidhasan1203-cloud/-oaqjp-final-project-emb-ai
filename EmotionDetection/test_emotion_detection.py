"""
test_emotion_detection.py

Unit tests for the EmotionDetection package. These tests call the live
Watson NLP service, matching the standard pattern used in this project.
Run with:

    python -m unittest test_emotion_detection.py
"""

import unittest

from EmotionDetection import emotion_detector


class TestEmotionDetection(unittest.TestCase):
    """Test suite verifying dominant-emotion detection for sample inputs."""

    def test_joy(self):
        """Text expressing gladness should be detected as joy."""
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')

    def test_anger(self):
        """Text expressing anger should be detected as anger."""
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result['dominant_emotion'], 'anger')

    def test_disgust(self):
        """Text expressing disgust should be detected as disgust."""
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result['dominant_emotion'], 'disgust')

    def test_sadness(self):
        """Text expressing sadness should be detected as sadness."""
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result['dominant_emotion'], 'sadness')

    def test_fear(self):
        """Text expressing fear should be detected as fear."""
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result['dominant_emotion'], 'fear')

    def test_returns_all_expected_keys(self):
        """The result dictionary should contain all five emotions plus the dominant one."""
        result = emotion_detector("I am glad this happened")
        expected_keys = {'anger', 'disgust', 'fear', 'joy', 'sadness', 'dominant_emotion'}
        self.assertEqual(set(result.keys()), expected_keys)

    def test_scores_are_floats(self):
        """Each emotion score should be returned as a float."""
        result = emotion_detector("I am glad this happened")
        for emotion in ('anger', 'disgust', 'fear', 'joy', 'sadness'):
            self.assertIsInstance(result[emotion], float)

    def test_blank_input_returns_none_values(self):
        """Blank input should produce a dictionary of None values, not an error."""
        result = emotion_detector("")
        for value in result.values():
            self.assertIsNone(value)

    def test_whitespace_input_returns_none_values(self):
        """Whitespace-only input should also produce a dictionary of None values."""
        result = emotion_detector("   ")
        for value in result.values():
            self.assertIsNone(value)


if __name__ == '__main__':
    unittest.main()
