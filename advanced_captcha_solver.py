import os
import time
import base64
import json
import random
import requests
import numpy as np
import cv2
from PIL import Image
import io
from typing import Tuple, List, Dict, Any, Optional
from captcha_patterns import PatternMatcher
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.console import Console

console = Console()

class AdvancedCaptchaSolver:
    def __init__(self):
        # Initialize all available solvers
        self.pattern_matcher = self._load_pattern_matcher()
        self.browser = None
        self.yolo_model = self._load_yolo_model()
        self.object_classes = self._load_object_classes()
        self.captcha_types = {
            "select_all_matching": ["Please select all", "Select all", "Choose all"],
            "select_specific": ["Please select", "Click on", "Choose the"],
            "verify_human": ["I'm not a robot", "I am human"]
        }
        
    def _load_pattern_matcher(self):
        """Initialize the basic pattern matcher"""
        try:
            pattern_matcher = PatternMatcher()
            console.print("[green]Successfully initialized pattern matcher[/green]")
            return pattern_matcher
        except Exception as e:
            console.print(f"[red]Error initializing pattern matcher: {str(e)}[/red]")
            return None
            
    def _load_yolo_model(self):
        """Load YOLO model for object detection if available"""
        try:
            # Check if we have OpenCV DNN
            has_dnn = hasattr(cv2, 'dnn')
            model_path = os.path.join(os.path.dirname(__file__), 'models')
            
            if has_dnn and os.path.exists(os.path.join(model_path, 'yolov3.weights')):
                # Load YOLOv3
                net = cv2.dnn.readNetFromDarknet(
                    os.path.join(model_path, 'yolov3.cfg'),
                    os.path.join(model_path, 'yolov3.weights')
                )
                console.print("[green]Successfully loaded YOLO model[/green]")
                return net
            else:
                # Download compact YOLOv3 if it doesn't exist
                if not os.path.exists(model_path):
                    os.makedirs(model_path)
                
                if not os.path.exists(os.path.join(model_path, 'yolov3-tiny.weights')):
                    console.print("[yellow]Downloading compact YOLO model...[/yellow]")
                    try:
                        os.system(f"curl -o {os.path.join(model_path, 'yolov3-tiny.weights')} https://pjreddie.com/media/files/yolov3-tiny.weights")
                        os.system(f"curl -o {os.path.join(model_path, 'yolov3-tiny.cfg')} https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg")
                    except:
                        console.print("[yellow]Failed to download YOLO model, will use pattern matching only[/yellow]")
                        return None
                
                if os.path.exists(os.path.join(model_path, 'yolov3-tiny.weights')):
                    net = cv2.dnn.readNetFromDarknet(
                        os.path.join(model_path, 'yolov3-tiny.cfg'),
                        os.path.join(model_path, 'yolov3-tiny.weights')
                    )
                    console.print("[green]Successfully loaded compact YOLO model[/green]")
                    return net
        except Exception as e:
            console.print(f"[yellow]Error loading YOLO model: {str(e)}. Will use pattern matching only.[/yellow]")
        
        return None
    
    def _load_object_classes(self):
        """Load object class names for models"""
        coco_classes = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 
                    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 
                    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 
                    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 
                    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 
                    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 
                    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 
                    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 
                    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 
                    'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']
                    
        # Common hCaptcha classes
        hcaptcha_classes = {
            'airplanes': ['airplane', 'aircraft', 'jet', 'plane'],
            'bicycles': ['bicycle', 'bike', 'cycling'],
            'boats': ['boat', 'ship', 'sailboat', 'watercraft'],
            'buses': ['bus', 'coach', 'autobus'],
            'cars': ['car', 'automobile', 'vehicle'],
            'motorcycles': ['motorcycle', 'motorbike', 'scooter'],
            'trains': ['train', 'locomotive', 'subway', 'metro'],
            'trucks': ['truck', 'lorry', 'pickup'],
            'animals': ['cat', 'dog', 'bird', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe'],
            'bridges': ['bridge', 'overpass', 'viaduct'],
            'chimneys': ['chimney', 'smokestack'],
            'crosswalks': ['crosswalk', 'zebra crossing', 'pedestrian crossing'],
            'fire hydrants': ['fire hydrant', 'hydrant'],
            'palm trees': ['palm tree', 'palm', 'coconut tree'],
            'parking meters': ['parking meter', 'meter'],
            'stairs': ['stairs', 'staircase', 'steps'],
            'stop signs': ['stop sign'],
            'traffic lights': ['traffic light', 'stoplight', 'signal']
        }
        
        return {
            'coco': coco_classes,
            'hcaptcha': hcaptcha_classes
        }

    def _preprocess_image(self, image_data):
        """Preprocess image for analysis"""
        try:
            # Convert base64 to image
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                image_data = base64.b64decode(image_data.split(',')[1])
            
            # Convert to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                console.print("[red]Failed to decode image[/red]")
                return None
                
            return img
        except Exception as e:
            console.print(f"[red]Error preprocessing image: {str(e)}[/red]")
            return None

    def _initialize_browser(self):
        """Initialize undetected Chrome browser"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            self.browser = uc.Chrome(options=options)
            console.print("[green]Browser initialized successfully[/green]")
        except Exception as e:
            console.print(f"[red]Error initializing browser: {str(e)}[/red]")
    
    def analyze_image_with_pattern_matcher(self, image):
        """Use pattern matching to analyze image"""
        results = {}
        if self.pattern_matcher:
            patterns = self.pattern_matcher.get_patterns()
            for name, pattern_ranges in patterns.items():
                if self.pattern_matcher.match_pattern(image, pattern_ranges):
                    results[name] = 0.7  # Standard confidence for pattern matches
        
        # Return the best match and confidence
        if results:
            best_match = max(results.items(), key=lambda x: x[1])
            return best_match[0], best_match[1]
        return None, 0.0
    
    def analyze_image_with_yolo(self, image):
        """Use YOLO model for object detection"""
        if self.yolo_model is None:
            return None, 0.0
            
        try:
            height, width = image.shape[:2]
            
            # Prepare image for YOLO
            blob = cv2.dnn.blobFromImage(image, 1/255.0, (416, 416), swapRB=True, crop=False)
            self.yolo_model.setInput(blob)
            
            # Get output layer names
            layer_names = self.yolo_model.getLayerNames()
            output_layers = [layer_names[i - 1] for i in self.yolo_model.getUnconnectedOutLayers()]
            
            # Run forward pass
            outputs = self.yolo_model.forward(output_layers)
            
            # Process outputs
            class_ids = []
            confidences = []
            
            for output in outputs:
                for detection in output:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    
                    if confidence > 0.5:  # Confidence threshold
                        class_ids.append(class_id)
                        confidences.append(float(confidence))
            
            # Get the most confident detection
            if confidences:
                max_conf_index = np.argmax(confidences)
                class_name = self.object_classes['coco'][class_ids[max_conf_index]]
                confidence = confidences[max_conf_index]
                
                # Map to hCaptcha classes
                for hcaptcha_class, aliases in self.object_classes['hcaptcha'].items():
                    if class_name in aliases:
                        return hcaptcha_class, confidence
                
                return class_name, confidence
                
        except Exception as e:
            console.print(f"[yellow]Error in YOLO analysis: {str(e)}[/yellow]")
            
        return None, 0.0
        
    # Cloud Vision functionality removed - not needed for core functionality
    
    def analyze_image(self, image):
        """Analyze image using multiple methods and return the most confident result"""
        results = []
        
        # Method 1: Pattern matching
        pattern_class, pattern_conf = self.analyze_image_with_pattern_matcher(image)
        if pattern_class:
            results.append((pattern_class, pattern_conf, "pattern"))
        
        # Method 2: YOLO
        yolo_class, yolo_conf = self.analyze_image_with_yolo(image)
        if yolo_class:
            results.append((yolo_class, yolo_conf, "yolo"))
        
        # Method 3: Cloud Vision support removed for simplification
        
        # Return the most confident result
        if results:
            results.sort(key=lambda x: x[1], reverse=True)
            console.print(f"[green]Best match: {results[0][0]} (Confidence: {results[0][1]:.2f}, Method: {results[0][2]})[/green]")
            return results[0][0], results[0][1]
        
        return None, 0.0
        
    def extract_captcha_type(self, captcha_text):
        """Extract the type of captcha from text"""
        captcha_text = captcha_text.lower()
        
        for captcha_type, patterns in self.captcha_types.items():
            if any(pattern.lower() in captcha_text for pattern in patterns):
                return captcha_type
                
        return "unknown"
    
    def extract_target_object(self, captcha_text):
        """Extract the target object from captcha text"""
        captcha_text = captcha_text.lower()
        
        # For specific selection captchas
        for hcaptcha_class in self.object_classes['hcaptcha'].keys():
            # Check singular form
            if hcaptcha_class.lower() in captcha_text:
                return hcaptcha_class
            # Check plural form by removing 's' if it exists
            if hcaptcha_class.lower().endswith('s') and hcaptcha_class[:-1].lower() in captcha_text:
                return hcaptcha_class
        
        # For general object detection
        for hcaptcha_class, aliases in self.object_classes['hcaptcha'].items():
            for alias in aliases:
                if alias.lower() in captcha_text:
                    return hcaptcha_class
                    
        return None

    def solve_captcha(self, site_key: str, site_url: str) -> Optional[str]:
        """Solve hCaptcha challenge and return the token"""
        try:
            console.print("[cyan]Initializing advanced AI captcha solver...[/cyan]")
            
            # Initialize browser if not already done
            if not self.browser:
                self._initialize_browser()
                if not self.browser:
                    return None
            
            # Navigate to hCaptcha
            self.browser.get(f"https://newassets.hcaptcha.com/captcha/v1/d11c9f2/static/hcaptcha-challenge.html#{site_key}")
            console.print("[cyan]Navigating to hCaptcha challenge...[/cyan]")
            
            # Wait for the challenge to load
            WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".challenge-container"))
            )
            console.print("[cyan]Challenge loaded, analyzing...[/cyan]")
            
            # Get the challenge text
            try:
                challenge_text = self.browser.find_element(By.CSS_SELECTOR, ".prompt-text").text
                console.print(f"[cyan]Challenge text: {challenge_text}[/cyan]")
                
                # Determine captcha type and target object
                captcha_type = self.extract_captcha_type(challenge_text)
                target_object = self.extract_target_object(challenge_text)
                
                console.print(f"[cyan]Detected captcha type: {captcha_type}, Target: {target_object}[/cyan]")
            except:
                console.print("[yellow]Could not find challenge text, using general solver[/yellow]")
                captcha_type = "unknown"
                target_object = None
            
            # Find all image elements
            img_elements = self.browser.find_elements(By.CSS_SELECTOR, ".task-image .image")
            if not img_elements:
                console.print("[yellow]No images found in the challenge[/yellow]")
                return None
                
            console.print(f"[cyan]Found {len(img_elements)} images to analyze[/cyan]")
            
            # Simple "I'm not a robot" verification
            if captcha_type == "verify_human":
                verify_btn = self.browser.find_element(By.CSS_SELECTOR, "#checkbox")
                verify_btn.click()
                time.sleep(2)
                
                # Get the hCaptcha token
                token = self.browser.execute_script("return document.getElementById('h-captcha-response').value")
                if token:
                    console.print("[green]Successfully solved 'I'm not a robot' challenge[/green]")
                    return token
            
            # Process each image for selection captchas
            for i, img in enumerate(img_elements):
                try:
                    # Extract image data
                    img_style = img.get_attribute("style")
                    img_url = img_style.split('url("')[1].split('")')[0]
                    
                    # Download the image
                    img_response = self.browser.execute_script(f"return fetch('{img_url}').then(r => r.blob()).then(blob => new Promise((resolve, reject) => {{const reader = new FileReader(); reader.onloadend = () => resolve(reader.result); reader.onerror = reject; reader.readAsDataURL(blob);}}))")
                    
                    # Process the image
                    processed_img = self._preprocess_image(img_response)
                    
                    if processed_img is not None:
                        # Analyze image
                        detected_class, confidence = self.analyze_image(processed_img)
                        
                        # Click on images that match the target class
                        if detected_class and target_object:
                            if (detected_class.lower() == target_object.lower() or 
                                detected_class.lower() in self.object_classes['hcaptcha'].get(target_object.lower(), [])):
                                console.print(f"[green]Image {i+1}: Found match for {target_object} (Confidence: {confidence:.2f})[/green]")
                                img.click()
                                time.sleep(0.5)
                        # If we don't have a target, click on any image with high confidence
                        elif detected_class and confidence > 0.7:
                            console.print(f"[green]Image {i+1}: Found {detected_class} (Confidence: {confidence:.2f})[/green]")
                            img.click()
                            time.sleep(0.5)
                            
                except Exception as e:
                    console.print(f"[yellow]Error processing image {i+1}: {str(e)}[/yellow]")
            
            # Submit the challenge
            submit_button = self.browser.find_element(By.CSS_SELECTOR, ".button-submit")
            submit_button.click()
            time.sleep(2)
            
            # Check if we need to solve more challenges
            try:
                new_challenge = self.browser.find_element(By.CSS_SELECTOR, ".challenge-container")
                console.print("[cyan]Additional challenge detected, solving...[/cyan]")
                return self.solve_captcha(site_key, site_url)  # Recursively solve new challenge
            except:
                pass
            
            # Get the hCaptcha token
            token = self.browser.execute_script("return document.getElementById('h-captcha-response').value")
            if token:
                console.print("[green]Successfully solved captcha challenge![/green]")
                return token
            else:
                console.print("[yellow]Could not find captcha token[/yellow]")
                return None
                
        except Exception as e:
            console.print(f"[red]Error in AI captcha solver: {str(e)}[/red]")
            console.print(f"[green]Buy Premium solver for 25$ [/green]")
            return None
            
    def close(self):
        """Close the browser"""
        if self.browser:
            self.browser.quit()
