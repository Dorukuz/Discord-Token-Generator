import cv2
import numpy as np

class PatternMatcher:
    @staticmethod
    def get_patterns():
        """Return common hCaptcha image patterns"""
        return {
            'airplane': [
                ([200, 200, 200], [255, 255, 255]),  # Sky color range
                ([100, 100, 100], [150, 150, 150])   # Aircraft body range
            ],
            'bicycle': [
                ([50, 50, 50], [100, 100, 100]),     # Wheel/frame color range
                ([150, 150, 150], [200, 200, 200])   # Background range
            ],
            'boat': [
                ([0, 100, 200], [100, 200, 255]),    # Water color range
                ([200, 200, 200], [255, 255, 255])   # Boat color range
            ],
            'bus': [
                ([200, 50, 50], [255, 100, 100]),    # Red bus color range
                ([50, 50, 200], [100, 100, 255])     # Blue bus color range
            ],
            'car': [
                ([50, 50, 50], [150, 150, 150]),     # Car body range
                ([200, 200, 200], [255, 255, 255])   # Road/background range
            ],
            'motorcycle': [
                ([0, 0, 0], [50, 50, 50]),          # Dark parts range
                ([200, 200, 200], [255, 255, 255])   # Chrome/metal range
            ],
            'train': [
                ([50, 50, 50], [100, 100, 100]),     # Train body range
                ([150, 150, 150], [200, 200, 200])   # Track/background range
            ],
            'truck': [
                ([100, 100, 100], [150, 150, 150]),  # Truck body range
                ([200, 200, 200], [255, 255, 255])   # Background range
            ]
        }

    @staticmethod
    def match_pattern(image, pattern_ranges):
        """Match image against a specific pattern's color ranges"""
        matches = 0
        for lower, upper in pattern_ranges:
            mask = cv2.inRange(image, np.array(lower), np.array(upper))
            if np.sum(mask) > 1000:  # Threshold for considering a match
                matches += 1
        return matches >= len(pattern_ranges) * 0.5  # 50% of ranges must match

    def analyze_image(self, image):
        """Analyze image and return best matching pattern"""
        patterns = self.get_patterns()
        best_match = None
        highest_confidence = 0

        for pattern_name, pattern_ranges in patterns.items():
            if self.match_pattern(image, pattern_ranges):
                confidence = 0.8  # Base confidence for pattern match
                if confidence > highest_confidence:
                    highest_confidence = confidence
                    best_match = pattern_name

        return best_match, highest_confidence
