#!/usr/bin/env python3
"""
GigaPrompter - Ultimate AI Image Prompt Generator
Enhanced with scientifically-backed attractiveness factors
Version: 2.0
"""

import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import random
import os
import platform
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import threading
import time

# Try importing clipboard libraries
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

# Enhanced VALUE_BANKS with scientific attractiveness factors
VALUE_BANKS = {
    "character": ["office worker", "social media influencer", "yoga instructor", "artist", "barista", "hiker", 
                  "fashion model", "nurse", "college student", "fitness trainer", "photographer", "dancer",
                  "entrepreneur", "scientist", "teacher", "designer", "chef", "musician"],
    
    "age": list(range(21, 36)),
    
    "ethnicity": ["caucasian", "black", "asian", "hispanic", "middle eastern", "indian", "latina", 
                  "mixed race", "mediterranean", "scandinavian", "eastern european", "brazilian",
                  "japanese", "korean", "thai", "vietnamese", "african american", "native american"],
    
    "beauty_level": ["stunning natural beauty", "striking model features", "ethereal elegance", 
                     "sultry and alluring", "girl-next-door charm", "radiant beauty", "exotic beauty", 
                     "classic beauty", "fresh-faced appeal", "sophisticated elegance", "captivating presence", 
                     "photogenic features", "timeless beauty", "magnetic charm", "effortless beauty"],
    
    # Scientifically-backed attractiveness factors
    "facial_symmetry": [
        "perfectly symmetrical features", "balanced facial proportions", 
        "harmonious bilateral symmetry", "flawlessly aligned features",
        "naturally symmetrical face", "mirror-perfect facial balance",
        "geometrically balanced features", "pristine facial symmetry"
    ],
    
    "facial_averageness": [
        "classically proportioned features", "population-average beauty", 
        "genetically diverse appearance", "heterozygous facial characteristics",
        "centrally clustered features", "universally appealing proportions",
        "balanced facial template", "archetypal beauty standards"
    ],
    
    "skin_health": [
        "radiant, healthy complexion", "clear, luminous skin texture", 
        "carotenoid-enhanced glow", "youthful skin elasticity",
        "even-toned, blemish-free skin", "porcelain-smooth texture",
        "vibrant, well-nourished skin", "naturally glowing complexion",
        "flawless skin clarity", "healthy blood flow visible"
    ],
    
    "femininity_traits": [
        "soft feminine features", "high estrogen characteristics", 
        "youthful facial adiposity", "feminine facial structure",
        "delicate bone structure", "graceful feminine contours",
        "refined feminine aesthetics", "elegant feminine proportions"
    ],
    
    "facial_dynamics": [
        "warm, natural smile", "expressive eye movements", 
        "dynamic facial expressiveness", "approachable demeanor",
        "genuine emotional expression", "captivating micro-expressions",
        "engaging facial animation", "authentic joy radiating",
        "charismatic presence", "emotionally intelligent expression"
    ],
    
    "facial_proportions": {
        "vertical": [
            "golden ratio facial thirds", "eye-mouth distance: 36% of face height", 
            "forehead proportion: 1/3 of face", "perfect vertical harmony",
            "ideal lower face proportions"
        ],
        "horizontal": [
            "interocular distance: 46% of face width", "nose width matches intercanthal distance",
            "mouth width: 1.5x nose width", "facial width follows phi ratio",
            "temple-to-temple golden proportion"
        ]
    },
    
    "neoteny_features": [
        "large, expressive eyes", "small, refined nose", "full, youthful lips",
        "smooth forehead curve", "soft facial contours", "childlike eye-to-face ratio",
        "button nose appeal", "doe-eyed innocence"
    ],
    
    "health_indicators": [
        "bright, clear sclera", "thick, lustrous hair", "strong nail beds",
        "healthy BMI range 18-24", "athletic posture", "vibrant energy",
        "natural vitality", "peak physical condition"
    ],
    
    "hair_color": ["jet black", "platinum blonde", "ash brown", "golden blonde", "fiery red", 
                   "chestnut brown", "auburn", "silver", "honey blonde", "dark chocolate", 
                   "caramel highlights", "strawberry blonde", "copper", "raven black", "mahogany",
                   "dirty blonde", "ombre blend", "balayage highlights"],
    
    "hair_style": ["flowing waves", "sleek straight", "messy bun", "high ponytail", "side-swept", 
                   "beach waves", "elegant updo", "loose curls", "braided crown", "tousled layers", 
                   "shoulder-length bob", "long layers", "french braid", "waterfall braid", 
                   "hollywood waves", "pixie cut", "long straight with bangs"],
    
    "eyes_color": ["bright blue", "emerald green", "warm hazel", "deep brown", "steel gray", 
                   "amber", "ocean blue", "forest green", "honey brown", "ice blue", 
                   "dark chocolate", "golden brown", "violet", "turquoise", "grey-green"],
    
    "eyes_description": ["captivating gaze", "expressive with long lashes", "bright and alert", 
                        "sultry bedroom eyes", "sparkling with life", "mysterious allure", 
                        "warm and inviting", "piercing intensity", "soft and gentle", 
                        "playful twinkle", "hypnotic depth", "innocent wide-eyed",
                        "seductive half-lidded", "bright with intelligence"],
    
    "lips_description": ["full pink lips", "natural rose", "glossy nude", "soft coral", 
                        "cherry tinted", "perfectly shaped", "subtle pink gloss", 
                        "natural fullness", "kissable pout", "elegant smile",
                        "cupid's bow defined", "plump and hydrated", "berry-stained"],
    
    "skin": {
        "color": ["porcelain", "olive", "golden tan", "deep ebony", "fair", "medium", 
                  "caramel", "bronze", "ivory", "honey", "warm beige", "sun-kissed",
                  "alabaster", "peachy", "cocoa", "tawny"],
        "texture": ["flawless", "dewy glow", "smooth", "radiant", "healthy luminance", 
                    "silk-like", "naturally perfect", "fresh", "velvet-soft", "matte perfection"],
        "quality": ["radiant", "glowing", "sun-kissed", "luminous", "healthy", "vibrant", 
                    "clear", "youthful", "pristine", "airbrushed", "naturally filtered"]
    },
    
    "body_type": {
        "waist": ["slim waist", "toned midsection", "naturally curved", "athletic core", 
                  "hourglass waist", "fit and trim", "slender", "defined abs", "tiny waist",
                  "sculpted core", "24-inch waist"],
        "bust": ["proportionate", "naturally full", "well-endowed", "generous curves", 
                 "perfect proportion", "feminine figure", "balanced silhouette", "natural C-cup",
                 "perky and firm", "ideal breast-to-body ratio"],
        "hips": ["curved hips", "feminine hips", "child-bearing hips", "shapely hips",
                 "0.7 waist-to-hip ratio", "brazilian curves", "athletic hips"],
        "overall": ["athletic and toned", "slender and graceful", "hourglass figure", 
                    "fit physique", "model proportions", "statuesque build", "petite and cute", 
                    "curves in all the right places", "dancer's body", "swimsuit ready",
                    "victoria's secret body", "gym-sculpted physique", "yoga-toned flexibility"]
    },
    
    "pose": {
        "position": ["standing confidently", "leaning casually", "sitting elegantly", 
                     "walking gracefully", "relaxed stance", "playful pose", "professional posture", 
                     "natural movement", "candid moment", "flirty stance", "power pose",
                     "model walk", "ballet-inspired pose", "lounging sensually"],
        "mood": ["confident smile", "mysterious allure", "joyful expression", "serene beauty", 
                 "playful energy", "sophisticated poise", "natural charm", "captivating presence", 
                 "relaxed comfort", "engaging warmth", "sultry gaze", "infectious laughter",
                 "thoughtful contemplation", "fierce determination"],
        "body_language": ["open and inviting", "closed and mysterious", "dynamic and energetic",
                         "relaxed and natural", "poised and elegant", "flirtatious and playful"],
        "hand_placement": ["on hips", "running through hair", "touching face gently", 
                          "crossed arms", "hands in pockets", "gesturing naturally"]
    },
    
    "costume": {
        "main_garment": {
            "type": ["fitted crop top", "stylish bikini", "elegant blouse", "sports bra", 
                     "cozy sweater", "summer sundress", "tank top", "off-shoulder top", 
                     "form-fitting dress", "casual t-shirt", "silk camisole", "wrap dress",
                     "bodycon dress", "cocktail dress", "evening gown", "blazer",
                     "leather jacket", "denim jacket", "lingerie set"],
            "style": ["trendy chic", "beach ready", "professional elegance", "athletic wear", 
                      "casual comfort", "feminine flow", "sporty casual", "evening elegance", 
                      "boho style", "minimalist", "vintage inspired", "modern contemporary",
                      "haute couture", "streetwear", "preppy", "grunge aesthetic"],
            "color": ["classic black", "pure white", "navy blue", "burgundy", "emerald green",
                     "royal purple", "blush pink", "fire red", "sunshine yellow", "nude/beige"],
            "material": ["silk", "cotton", "lace", "leather", "denim", "cashmere", "satin",
                        "velvet", "chiffon", "modal", "athletic fabric"],
            "fit": ["perfectly tailored", "body-hugging", "loose and flowing", "form-fitting",
                   "relaxed fit", "skin-tight", "draped elegantly"],
            "neckline": ["strapless", "halter", "v-neck", "scoop", "off-shoulder", 
                        "sweetheart", "high neck", "one-shoulder", "plunging", "boat neck",
                        "cowl neck", "square neck", "keyhole"],
            "special_features": ["perfect fit", "flowing fabric", "figure-hugging", 
                               "breathable material", "designer quality", "luxurious texture", 
                               "flattering cut", "trendy design", "revealing cutouts",
                               "strategic transparency", "embellished details"]
        },
        "bottoms": {
            "type": ["designer jeans", "mini skirt", "yoga pants", "denim shorts", 
                     "flowing skirt", "leather pants", "high-waisted shorts", "pencil skirt", 
                     "leggings", "palazzo pants", "hot pants", "maxi skirt", "biker shorts",
                     "tennis skirt", "cargo pants"],
            "description": ["form-fitting", "perfectly tailored", "figure-flattering", 
                           "trendy style", "comfortable fit", "fashionable cut", "sexy fit", 
                           "elegant drape", "skin-tight", "high-waisted", "low-rise"]
        },
        "footwear": {
            "type": ["high heels", "designer sneakers", "ankle boots", "strappy sandals", 
                     "platform heels", "ballet flats", "knee-high boots", "wedges", "pumps",
                     "stilettos", "combat boots", "over-knee boots", "loafers", "mules"],
            "heel_height": ["flat", "kitten heel", "3-inch", "4-inch", "5-inch", "platform"],
            "special_features": ["designer brand", "perfect fit", "stylish design", 
                               "comfortable", "eye-catching", "elegant", "trendy", "classic style",
                               "red bottom soles", "crystal embellished"]
        },
        "accessories": {
            "neck": ["delicate necklace", "gold chain", "silver pendant", "choker", 
                     "layered chains", "diamond necklace", "pearl strand", "statement piece"],
            "wrists": ["elegant bracelet", "designer watch", "gold bangle", "tennis bracelet", 
                      "fitness tracker", "charm bracelet", "cuff bracelet", "stack of bangles"],
            "fingers": ["diamond ring", "elegant bands", "minimalist ring", "statement ring", 
                       "engagement ring", "midi rings", "cocktail ring"],
            "ears": ["diamond studs", "gold hoops", "drop earrings", "pearl earrings", 
                    "elegant dangles", "small studs", "chandelier earrings", "ear cuffs"],
            "other": ["designer handbag", "silk scarf", "sunglasses", "belt", "hat", "anklet"]
        }
    },
    
    "background": {
        "setting": ["photo studio", "beach paradise", "urban cityscape", "luxury interior", 
                   "natural outdoors", "modern office", "cozy bedroom", "rooftop terrace", 
                   "poolside", "cafe setting", "nightclub", "art gallery", "fashion runway",
                   "tropical resort", "mountain vista", "paris street", "tokyo neon district"],
        "atmosphere": ["professional lighting", "golden hour glow", "soft natural light", 
                      "vibrant energy", "intimate ambiance", "glamorous setting", "relaxed vibe", 
                      "romantic mood", "dynamic scene", "dreamy atmosphere", "moody lighting",
                      "cinematic quality", "ethereal glow", "dramatic shadows"],
        "time_of_day": ["sunrise", "morning", "noon", "golden hour", "sunset", "blue hour", 
                       "night", "midnight"],
        "weather": ["clear sky", "partly cloudy", "overcast", "misty", "after rain", "snow"],
        "elements": ["professional setup", "natural scenery", "city skyline", "elegant decor", 
                    "soft lighting", "modern architecture", "tropical plants", "sunset backdrop", 
                    "bokeh lights", "minimalist background", "neon signs", "water reflections",
                    "lens flares", "floating particles"]
    },
    
    "composition": {
        "framing": ["professional portrait", "full body shot", "upper body focus", 
                   "candid capture", "three-quarter angle", "profile view", "dynamic angle", 
                   "fashion pose", "hero shot", "dutch angle", "bird's eye view", "worm's eye view"],
        "range": ["full length", "waist up", "chest up", "close portrait", "mid-thigh up", 
                 "shoulders up", "full figure", "extreme close-up", "medium shot", "wide shot"],
        "focal_point": ["eyes in focus", "face centered", "body emphasized", "outfit highlight",
                       "gesture focus", "emotion captured"],
        "depth_of_field": ["shallow DOF", "deep focus", "bokeh background", "tilt-shift effect",
                          "selective focus", "f/1.4 aperture", "f/2.8 aperture"],
        "rule_application": ["rule of thirds", "golden ratio", "leading lines", "symmetry",
                            "frame within frame", "patterns", "negative space"]
    },
    
    "photo_style": {
        "genre": ["fashion", "portrait", "lifestyle", "glamour", "editorial", "commercial",
                 "beauty", "fitness", "artistic", "candid", "street style", "high fashion"],
        "influence": ["Vogue", "Harper's Bazaar", "Sports Illustrated", "Victoria's Secret",
                     "Maxim", "GQ", "Elle", "Cosmopolitan", "Marie Claire"],
        "photographer_style": ["Annie Leibovitz", "Mario Testino", "Peter Lindbergh", 
                              "Steven Meisel", "Patrick Demarchelier", "Terry Richardson"],
        "processing": ["raw and natural", "heavily retouched", "film emulation", "HDR",
                      "black and white", "vintage filter", "modern clean edit", "cinematic grade"],
        "camera": ["Canon 5D Mark IV", "Nikon D850", "Sony A7R IV", "Hasselblad X1D",
                  "Phase One XF", "Leica M10", "Fujifilm GFX100", "RED Digital Cinema"],
        "lens": ["85mm f/1.4", "50mm f/1.2", "35mm f/1.4", "70-200mm f/2.8", 
                "24-70mm f/2.8", "135mm f/2", "200mm f/2"],
        "lighting_setup": ["three-point lighting", "Rembrandt lighting", "butterfly lighting",
                          "split lighting", "loop lighting", "broad lighting", "short lighting",
                          "high-key", "low-key", "natural light only"]
    },
    
    "priority_instructions": [
        "Focus on photorealistic quality with perfect skin rendering",
        "Emphasize natural beauty with scientific proportion accuracy",
        "Professional photography standards with magazine-quality output",
        "Perfect lighting and composition following golden ratio",
        "Highlight attractive features using proven aesthetic principles",
        "Fashion-forward styling with current trend awareness",
        "Flawless execution with attention to every detail",
        "Create aspirational imagery with emotional impact",
        "Ensure technical perfection in focus and exposure",
        "Maximize visual appeal through proven attractiveness factors"
    ]
}

# Enhanced templates for different AI models
AI_TEMPLATES = {
    "grok_detailed": "Photorealistic portrait: {age}-year-old {ethnicity} woman with {beauty_level}. {symmetry}, {skin_health}. {hair}, {eyes}, {lips}. {body_type}. Wearing {outfit}. {pose} in {setting}. {quality}, {style}",
    "grok_simple": "{ethnicity} woman, {age}, {beauty_level}, {outfit}, {quality} photo",
    "midjourney": "/imagine prompt: {beauty_level} {age}yo {ethnicity} woman, {hair}, {eyes}, {body_type}, wearing {outfit}, {pose}, {background}, {lighting}, {style} --ar 2:3 --q 2 --v 6",
    "dalle3": "Professional photograph of a {age}-year-old {ethnicity} woman with {beauty_level}, {symmetry}, {skin_health}. She has {hair} and {eyes}. {body_type} wearing {outfit}. {pose} with {mood}. Background: {setting} with {atmosphere}. Shot with {camera} using {lighting}",
    "stable_diffusion": "((best quality)), ((masterpiece)), ((realistic)), {age}yo {ethnicity} woman, {beauty_level}, {symmetry}, {skin_health}, {hair}, {eyes}, {lips}, {body_type}, wearing {outfit}, {pose}, {setting}, {lighting}, professional photography, 8k uhd, dslr, high quality, film grain",
    "leonardo": "Hyper-realistic {age} year old {ethnicity} female, {beauty_level}, {facial_dynamics}, {skin_health}, {hair} hair, {eyes} eyes, {body_type}, wearing {outfit}, {pose} pose, {background} setting, {lighting} lighting, photorealistic, 8k resolution",
    "flux": "Beautiful {ethnicity} woman aged {age}, exhibiting {beauty_level} with {symmetry} and {averageness}. Features: {hair}, {eyes}, {lips}, {skin_health}. Body: {body_type}. Outfit: {outfit}. Pose: {pose} with {mood}. Environment: {setting}, {atmosphere}. Photography style: {quality}, {style}"
}

# Enhanced presets with attractiveness factors
PRESET_LOOKS = {
    "Instagram Influencer": {
        "beauty_level": "stunning natural beauty",
        "facial_symmetry": "perfectly symmetrical features",
        "skin_health": "radiant, healthy complexion",
        "facial_dynamics": "warm, natural smile",
        "photo_quality": "ultra high resolution",
        "style_reference": "Instagram influencer",
        "pose_mood": "confident smile",
        "background_atmosphere": "golden hour glow",
        "neoteny": "large, expressive eyes"
    },
    "Fashion Model": {
        "character": "fashion model",
        "beauty_level": "striking model features",
        "facial_symmetry": "flawlessly aligned features",
        "facial_averageness": "classically proportioned features",
        "body_overall": "model proportions",
        "photo_quality": "magazine quality",
        "style_reference": "Vogue photoshoot",
        "lighting_type": "studio lighting",
        "composition_framing": "fashion pose"
    },
    "Beach Goddess": {
        "character": "social media influencer",
        "main_garment_type": "stylish bikini",
        "background_setting": "beach paradise",
        "hair_style": "beach waves",
        "skin_quality": "sun-kissed",
        "skin_health": "carotenoid-enhanced glow",
        "facial_dynamics": "playful energy",
        "body_overall": "swimsuit ready"
    },
    "Corporate Professional": {
        "character": "office worker",
        "main_garment_type": "elegant blouse",
        "photo_quality": "professional photography",
        "background_setting": "modern office",
        "pose_position": "professional posture",
        "facial_averageness": "universally appealing proportions",
        "facial_dynamics": "confident, approachable expression"
    },
    "Fitness Goddess": {
        "character": "fitness trainer",
        "body_overall": "athletic and toned",
        "main_garment_type": "sports bra",
        "background_setting": "modern gym",
        "pose_mood": "energetic vibe",
        "skin_health": "vibrant, well-nourished skin",
        "health_indicators": "peak physical condition"
    },
    "Evening Elegance": {
        "beauty_level": "sophisticated elegance",
        "main_garment_type": "evening gown",
        "background_setting": "luxury interior",
        "facial_symmetry": "harmonious bilateral symmetry",
        "femininity_traits": "refined feminine aesthetics",
        "pose_mood": "sophisticated poise",
        "lighting_type": "dramatic lighting"
    },
    "Natural Beauty": {
        "beauty_level": "girl-next-door charm",
        "facial_dynamics": "genuine emotional expression",
        "skin_health": "naturally glowing complexion",
        "main_garment_type": "casual t-shirt",
        "pose_mood": "relaxed comfort",
        "background_atmosphere": "soft natural light"
    },
    "Artistic Portrait": {
        "character": "artist",
        "beauty_level": "ethereal elegance",
        "facial_proportions": "golden ratio facial thirds",
        "photo_quality": "artistic composition",
        "lighting_type": "Rembrandt lighting",
        "composition_framing": "three-quarter angle"
    }
}

# Negative prompts for different AI models
NEGATIVE_PROMPTS = {
    "default": "ugly, deformed, bad anatomy, blurry, low quality, watermark, text, logo, bad hands, missing fingers, extra digits, poorly drawn face, mutation, mutated, worst quality, low resolution, grainy, signature",
    "realistic": "cartoon, anime, drawing, sketch, painting, illustration, 3d render, cgi, render, digital art, artstation, concept art, abstract",
    "clean": "explicit, nude, nsfw, revealing, inappropriate, suggestive, violence, gore, blood",
    "professional": "amateur, poor lighting, bad composition, unflattering angle, out of focus, motion blur, overexposed, underexposed, bad white balance",
    "midjourney": "--no ugly, deformed, noisy, blurry, distorted, grainy, text, watermark, signature",
    "stable_diffusion": "((worst quality)), ((low quality)), ((normal quality)), lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, jpeg artifacts, signature, watermark, username, blurry, artist name, (bad_prompt:0.8), multiple views, multiple panels, blurry, watermark, letterbox, text"
}

class CrossPlatformHelper:
    """Helper class for cross-platform compatibility"""
    
    @staticmethod
    def get_save_directory():
        """Get appropriate save directory for current platform"""
        system = platform.system()
        
        if system == "Windows":
            base_path = Path.home() / "Documents" / "GigaPrompter"
        elif system == "Linux" and "ANDROID_ROOT" in os.environ:
            base_path = Path("/storage/emulated/0/Documents/GigaPrompter")
        else:
            base_path = Path.home() / "GigaPrompter"
        
        output_path = base_path / "outputs"
        favorites_path = base_path / "favorites"
        presets_path = base_path / "presets"
        
        for path in [output_path, favorites_path, presets_path]:
            path.mkdir(parents=True, exist_ok=True)
        
        return base_path, output_path, favorites_path, presets_path
    
    @staticmethod
    def copy_to_clipboard(text, root):
        """Cross-platform clipboard copy"""
        success = False
        method = ""
        
        if HAS_PYPERCLIP:
            try:
                pyperclip.copy(text)
                success = True
                method = "pyperclip"
            except:
                pass
        
        if not success:
            try:
                root.clipboard_clear()
                root.clipboard_append(text)
                root.update()
                success = True
                method = "tkinter"
            except:
                pass
        
        if not success and platform.system() == "Windows":
            try:
                import subprocess
                subprocess.run(['clip'], input=text, text=True, check=True)
                success = True
                method = "Windows clip"
            except:
                pass
        
        return success, method

class FavoritesManager:
    """Manage favorite prompt combinations"""
    
    def __init__(self, favorites_path):
        self.favorites_path = favorites_path / "favorites.json"
        self.favorites = self.load_favorites()
    
    def load_favorites(self):
        """Load favorites from file"""
        if self.favorites_path.exists():
            try:
                with open(self.favorites_path, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def save_favorite(self, name, prompt_dict, plain_text):
        """Save a favorite prompt"""
        favorite = {
            "name": name,
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt_dict,
            "plain_text": plain_text
        }
        self.favorites.append(favorite)
        
        with open(self.favorites_path, 'w') as f:
            json.dump(self.favorites, f, indent=2)
        
        return True
    
    def get_favorite_names(self):
        """Get list of favorite names"""
        return [f["name"] for f in self.favorites]
    
    def load_favorite(self, name):
        """Load a specific favorite"""
        for fav in self.favorites:
            if fav["name"] == name:
                return fav
        return None
    
    def delete_favorite(self, name):
        """Delete a favorite"""
        self.favorites = [f for f in self.favorites if f["name"] != name]
        with open(self.favorites_path, 'w') as f:
            json.dump(self.favorites, f, indent=2)

class PromptHistory:
    """Manage prompt generation history"""
    
    def __init__(self, max_size=50):
        self.history = []
        self.max_size = max_size
        self.current_index = -1
    
    def add(self, prompt_dict, plain_text):
        """Add prompt to history"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt_dict,
            "plain_text": plain_text
        }
        self.history.append(entry)
        if len(self.history) > self.max_size:
            self.history.pop(0)
        self.current_index = len(self.history) - 1
    
    def get_previous(self):
        """Get previous prompt from history"""
        if self.current_index > 0:
            self.current_index -= 1
            return self.history[self.current_index]
        return None
    
    def get_next(self):
        """Get next prompt from history"""
        if self.current_index < len(self.history) - 1:
            self.current_index += 1
            return self.history[self.current_index]
        return None

def generate_prompt(theme=None, custom_values=None):
    """Enhanced prompt generation with attractiveness factors"""
    if custom_values is None:
        custom_values = {}
    
    prompt = {
        "image_prompt": {
            "subject": {
                "character": "",
                "physical_attributes": {
                    "age": None,
                    "ethnicity": "",
                    "beauty_level": "",
                    "hair": {"color": "", "style": ""},
                    "eyes": {"color": "", "description": ""},
                    "lips": {"description": ""},
                    "skin": {"color": "", "texture": "", "quality": ""},
                    "body_type": {"waist": "", "bust": "", "hips": "", "overall": ""},
                    "pose": {"position": "", "mood": "", "body_language": "", "hand_placement": ""},
                    "attractiveness_factors": {
                        "symmetry": "",
                        "averageness": "",
                        "skin_health": "",
                        "femininity": "",
                        "dynamics": "",
                        "proportions": [],
                        "neoteny": "",
                        "health_indicators": ""
                    }
                },
                "costume": {
                    "main_garment": {
                        "type": "", "style": "", "color": "", "material": "", 
                        "fit": "", "neckline": "", "special_features": ""
                    },
                    "bottoms": {"type": "", "description": ""},
                    "footwear": {"type": "", "heel_height": "", "special_features": ""},
                    "accessories": {"neck": "", "wrists": "", "fingers": "", "ears": "", "other": ""}
                }
            },
            "background": {
                "setting": "", "atmosphere": "", "time_of_day": "", 
                "weather": "", "elements": []
            },
            "composition": {
                "framing": "", "range": "", "focal_point": "", 
                "depth_of_field": "", "rule_application": ""
            },
            "photo_style": {
                "genre": "", "influence": "", "photographer_style": "", 
                "processing": "", "camera": "", "lens": "", "lighting_setup": ""
            },
            "priority_instructions": ""
        }
    }
    
    # Apply custom values or random selection - Basic attributes
    prompt['image_prompt']['subject']['character'] = custom_values.get('character', random.choice(VALUE_BANKS["character"]))
    prompt['image_prompt']['subject']['physical_attributes']['age'] = custom_values.get('age', random.choice(VALUE_BANKS["age"]))
    prompt['image_prompt']['subject']['physical_attributes']['ethnicity'] = custom_values.get('ethnicity', random.choice(VALUE_BANKS["ethnicity"]))
    prompt['image_prompt']['subject']['physical_attributes']['beauty_level'] = custom_values.get('beauty_level', random.choice(VALUE_BANKS["beauty_level"]))
    
    # Hair, eyes, lips
    prompt['image_prompt']['subject']['physical_attributes']['hair']['color'] = custom_values.get('hair_color', random.choice(VALUE_BANKS["hair_color"]))
    prompt['image_prompt']['subject']['physical_attributes']['hair']['style'] = custom_values.get('hair_style', random.choice(VALUE_BANKS["hair_style"]))
    prompt['image_prompt']['subject']['physical_attributes']['eyes']['color'] = custom_values.get('eyes_color', random.choice(VALUE_BANKS["eyes_color"]))
    prompt['image_prompt']['subject']['physical_attributes']['eyes']['description'] = custom_values.get('eyes_description', random.choice(VALUE_BANKS["eyes_description"]))
    prompt['image_prompt']['subject']['physical_attributes']['lips']['description'] = custom_values.get('lips_description', random.choice(VALUE_BANKS["lips_description"]))
    
    # Skin attributes
    prompt['image_prompt']['subject']['physical_attributes']['skin']['color'] = custom_values.get('skin_color', random.choice(VALUE_BANKS["skin"]["color"]))
    prompt['image_prompt']['subject']['physical_attributes']['skin']['texture'] = custom_values.get('skin_texture', random.choice(VALUE_BANKS["skin"]["texture"]))
    prompt['image_prompt']['subject']['physical_attributes']['skin']['quality'] = custom_values.get('skin_quality', random.choice(VALUE_BANKS["skin"]["quality"]))
    
    # Body type
    prompt['image_prompt']['subject']['physical_attributes']['body_type']['waist'] = custom_values.get('waist', random.choice(VALUE_BANKS["body_type"]["waist"]))
    prompt['image_prompt']['subject']['physical_attributes']['body_type']['bust'] = custom_values.get('bust', random.choice(VALUE_BANKS["body_type"]["bust"]))
    prompt['image_prompt']['subject']['physical_attributes']['body_type']['hips'] = custom_values.get('hips', random.choice(VALUE_BANKS["body_type"]["hips"]))
    prompt['image_prompt']['subject']['physical_attributes']['body_type']['overall'] = custom_values.get('body_overall', random.choice(VALUE_BANKS["body_type"]["overall"]))
    
    # Pose
    prompt['image_prompt']['subject']['physical_attributes']['pose']['position'] = custom_values.get('pose_position', random.choice(VALUE_BANKS["pose"]["position"]))
    prompt['image_prompt']['subject']['physical_attributes']['pose']['mood'] = custom_values.get('pose_mood', random.choice(VALUE_BANKS["pose"]["mood"]))
    prompt['image_prompt']['subject']['physical_attributes']['pose']['body_language'] = custom_values.get('body_language', random.choice(VALUE_BANKS["pose"]["body_language"]))
    prompt['image_prompt']['subject']['physical_attributes']['pose']['hand_placement'] = custom_values.get('hand_placement', random.choice(VALUE_BANKS["pose"]["hand_placement"]))
    
    # Attractiveness factors
    af = prompt['image_prompt']['subject']['physical_attributes']['attractiveness_factors']
    af['symmetry'] = custom_values.get('facial_symmetry', random.choice(VALUE_BANKS["facial_symmetry"]))
    af['averageness'] = custom_values.get('facial_averageness', random.choice(VALUE_BANKS["facial_averageness"]))
    af['skin_health'] = custom_values.get('skin_health', random.choice(VALUE_BANKS["skin_health"]))
    af['femininity'] = custom_values.get('femininity_traits', random.choice(VALUE_BANKS["femininity_traits"]))
    af['dynamics'] = custom_values.get('facial_dynamics', random.choice(VALUE_BANKS["facial_dynamics"]))
    af['neoteny'] = custom_values.get('neoteny_features', random.choice(VALUE_BANKS["neoteny_features"]))
    af['health_indicators'] = custom_values.get('health_indicators', random.choice(VALUE_BANKS["health_indicators"]))
    af['proportions'] = [
        random.choice(VALUE_BANKS["facial_proportions"]["vertical"]),
        random.choice(VALUE_BANKS["facial_proportions"]["horizontal"])
    ]
    
    # Costume
    costume = prompt['image_prompt']['subject']['costume']
    costume['main_garment']['type'] = custom_values.get('main_garment_type', random.choice(VALUE_BANKS["costume"]["main_garment"]["type"]))
    costume['main_garment']['style'] = custom_values.get('main_garment_style', random.choice(VALUE_BANKS["costume"]["main_garment"]["style"]))
    costume['main_garment']['color'] = custom_values.get('main_garment_color', random.choice(VALUE_BANKS["costume"]["main_garment"]["color"]))
    costume['main_garment']['material'] = custom_values.get('main_garment_material', random.choice(VALUE_BANKS["costume"]["main_garment"]["material"]))
    costume['main_garment']['fit'] = custom_values.get('main_garment_fit', random.choice(VALUE_BANKS["costume"]["main_garment"]["fit"]))
    costume['main_garment']['neckline'] = random.choice(VALUE_BANKS["costume"]["main_garment"]["neckline"])
    costume['main_garment']['special_features'] = random.choice(VALUE_BANKS["costume"]["main_garment"]["special_features"])
    
    costume['bottoms']['type'] = custom_values.get('bottoms_type', random.choice(VALUE_BANKS["costume"]["bottoms"]["type"]))
    costume['bottoms']['description'] = random.choice(VALUE_BANKS["costume"]["bottoms"]["description"])
    
    costume['footwear']['type'] = custom_values.get('footwear_type', random.choice(VALUE_BANKS["costume"]["footwear"]["type"]))
    costume['footwear']['heel_height'] = random.choice(VALUE_BANKS["costume"]["footwear"]["heel_height"])
    costume['footwear']['special_features'] = random.choice(VALUE_BANKS["costume"]["footwear"]["special_features"])
    
    # Accessories
    costume['accessories']['neck'] = random.choice(VALUE_BANKS["costume"]["accessories"]["neck"])
    costume['accessories']['wrists'] = random.choice(VALUE_BANKS["costume"]["accessories"]["wrists"])
    costume['accessories']['fingers'] = random.choice(VALUE_BANKS["costume"]["accessories"]["fingers"])
    costume['accessories']['ears'] = random.choice(VALUE_BANKS["costume"]["accessories"]["ears"])
    costume['accessories']['other'] = random.choice(VALUE_BANKS["costume"]["accessories"]["other"])
    
    # Background
    bg = prompt['image_prompt']['background']
    bg['setting'] = custom_values.get('background_setting', random.choice(VALUE_BANKS["background"]["setting"]))
    bg['atmosphere'] = custom_values.get('background_atmosphere', random.choice(VALUE_BANKS["background"]["atmosphere"]))
    bg['time_of_day'] = custom_values.get('time_of_day', random.choice(VALUE_BANKS["background"]["time_of_day"]))
    bg['weather'] = custom_values.get('weather', random.choice(VALUE_BANKS["background"]["weather"]))
    bg['elements'] = random.choices(VALUE_BANKS["background"]["elements"], k=3)
    
    # Composition
    comp = prompt['image_prompt']['composition']
    comp['framing'] = custom_values.get('composition_framing', random.choice(VALUE_BANKS["composition"]["framing"]))
    comp['range'] = custom_values.get('composition_range', random.choice(VALUE_BANKS["composition"]["range"]))
    comp['focal_point'] = custom_values.get('focal_point', random.choice(VALUE_BANKS["composition"]["focal_point"]))
    comp['depth_of_field'] = custom_values.get('depth_of_field', random.choice(VALUE_BANKS["composition"]["depth_of_field"]))
    comp['rule_application'] = custom_values.get('rule_application', random.choice(VALUE_BANKS["composition"]["rule_application"]))
    
    # Photo style
    ps = prompt['image_prompt']['photo_style']
    ps['genre'] = custom_values.get('photo_genre', random.choice(VALUE_BANKS["photo_style"]["genre"]))
    ps['influence'] = custom_values.get('style_influence', random.choice(VALUE_BANKS["photo_style"]["influence"]))
    ps['photographer_style'] = custom_values.get('photographer_style', random.choice(VALUE_BANKS["photo_style"]["photographer_style"]))
    ps['processing'] = custom_values.get('processing', random.choice(VALUE_BANKS["photo_style"]["processing"]))
    ps['camera'] = custom_values.get('camera', random.choice(VALUE_BANKS["photo_style"]["camera"]))
    ps['lens'] = custom_values.get('lens', random.choice(VALUE_BANKS["photo_style"]["lens"]))
    ps['lighting_setup'] = custom_values.get('lighting_setup', random.choice(VALUE_BANKS["photo_style"]["lighting_setup"]))
    
    prompt['image_prompt']['priority_instructions'] = random.choice(VALUE_BANKS["priority_instructions"])
    
    return prompt

def create_ai_optimized_prompt(json_prompt, template="grok_detailed", include_negative=False):
    """Create AI-optimized prompt from JSON for various models"""
    
    subj = json_prompt['image_prompt']['subject']
    pa = subj['physical_attributes']
    af = pa['attractiveness_factors']
    costume = subj['costume']
    bg = json_prompt['image_prompt']['background']
    comp = json_prompt['image_prompt']['composition']
    ps = json_prompt['image_prompt']['photo_style']
    
    # Build component strings
    hair_desc = f"{pa['hair']['color']} hair in {pa['hair']['style']}"
    eyes_desc = f"{pa['eyes']['color']} eyes with {pa['eyes']['description']}"
    body_desc = f"{pa['body_type']['overall']} with {pa['body_type']['bust']} and {pa['body_type']['waist']}"
    outfit_desc = f"{costume['main_garment']['color']} {costume['main_garment']['type']} ({costume['main_garment']['style']}, {costume['main_garment']['fit']}) with {costume['bottoms']['type']}"
    pose_desc = f"{pa['pose']['mood']} while {pa['pose']['position']}, {pa['pose']['body_language']}"
    
    if template == "grok_detailed":
        prompt = f"Photorealistic portrait: {pa['age']}-year-old {pa['ethnicity']} woman with {pa['beauty_level']}. "
        prompt += f"{af['symmetry']} with {af['averageness']}. {af['skin_health']} and {af['femininity']}. "
        prompt += f"{hair_desc}, {eyes_desc}, {pa['lips']['description']}. "
        prompt += f"{pa['skin']['quality']} {pa['skin']['color']} skin with {pa['skin']['texture']} texture. "
        prompt += f"{body_desc}. {af['neoteny']} showing {af['health_indicators']}. "
        prompt += f"Wearing {outfit_desc}. {costume['footwear']['type']} shoes. "
        prompt += f"{pose_desc}. "
        prompt += f"{bg['setting']} background with {bg['atmosphere']} during {bg['time_of_day']}. "
        prompt += f"Shot with {ps['camera']} using {ps['lens']} lens. {ps['lighting_setup']} lighting. "
        prompt += f"{ps['genre']} photography style influenced by {ps['influence']}. "
        prompt += f"Captured with {af['dynamics']}. Facial proportions: {', '.join(af['proportions'])}."
    
    elif template == "grok_simple":
        prompt = f"{pa['ethnicity']} woman, {pa['age']}, {pa['beauty_level']}, "
        prompt += f"wearing {costume['main_garment']['type']}, "
        prompt += f"{ps['genre']} photography"
    
    elif template == "midjourney":
        prompt = f"/imagine prompt: {pa['beauty_level']} {pa['age']}yo {pa['ethnicity']} woman, "
        prompt += f"{af['symmetry']}, {af['skin_health']}, {hair_desc}, {eyes_desc}, "
        prompt += f"{body_desc}, wearing {outfit_desc}, "
        prompt += f"{pose_desc}, {bg['setting']} with {bg['atmosphere']}, "
        prompt += f"{ps['lighting_setup']}, {ps['genre']} style by {ps['photographer_style']} "
        prompt += "--ar 2:3 --q 2 --v 6"
    
    elif template == "dalle3":
        prompt = f"Professional photograph of a {pa['age']}-year-old {pa['ethnicity']} woman with {pa['beauty_level']}, "
        prompt += f"{af['symmetry']}, {af['skin_health']}. She has {hair_desc} and {eyes_desc}. "
        prompt += f"{body_desc} wearing {outfit_desc}. "
        prompt += f"{pose_desc} with {af['dynamics']}. "
        prompt += f"Background: {bg['setting']} with {bg['atmosphere']} during {bg['time_of_day']}. "
        prompt += f"Shot with {ps['camera']} using {ps['lens']}, {ps['lighting_setup']} lighting"
    
    elif template == "stable_diffusion":
        prompt = f"((best quality)), ((masterpiece)), ((realistic)), "
        prompt += f"{pa['age']}yo {pa['ethnicity']} woman, {pa['beauty_level']}, "
        prompt += f"{af['symmetry']}, {af['skin_health']}, {af['femininity']}, "
        prompt += f"{hair_desc}, {eyes_desc}, {pa['lips']['description']}, "
        prompt += f"{body_desc}, wearing {outfit_desc}, "
        prompt += f"{pose_desc}, {bg['setting']}, {ps['lighting_setup']}, "
        prompt += f"professional {ps['genre']} photography, 8k uhd, dslr, high quality, film grain"
    
    elif template == "leonardo":
        prompt = f"Hyper-realistic {pa['age']} year old {pa['ethnicity']} female, "
        prompt += f"{pa['beauty_level']}, {af['dynamics']}, {af['skin_health']}, "
        prompt += f"{hair_desc}, {eyes_desc}, {body_desc}, "
        prompt += f"wearing {outfit_desc}, {pose_desc}, "
        prompt += f"{bg['setting']} setting, {ps['lighting_setup']} lighting, "
        prompt += f"photorealistic, 8k resolution, {ps['genre']} photography"
    
    elif template == "flux":
        prompt = f"Beautiful {pa['ethnicity']} woman aged {pa['age']}, "
        prompt += f"exhibiting {pa['beauty_level']} with {af['symmetry']} and {af['averageness']}. "
        prompt += f"Features: {hair_desc}, {eyes_desc}, {pa['lips']['description']}, {af['skin_health']}. "
        prompt += f"Body: {body_desc}. Outfit: {outfit_desc}. "
        prompt += f"Pose: {pose_desc} with {af['dynamics']}. "
        prompt += f"Environment: {bg['setting']}, {bg['atmosphere']} at {bg['time_of_day']}. "
        prompt += f"Photography style: {ps['genre']}, shot with {ps['camera']}"
    
    # Add negative prompt if requested
    if include_negative:
        if "midjourney" in template:
            neg_prompt = NEGATIVE_PROMPTS["midjourney"]
        elif "stable_diffusion" in template:
            neg_prompt = NEGATIVE_PROMPTS["stable_diffusion"]
        else:
            neg_prompt = NEGATIVE_PROMPTS.get("realistic", NEGATIVE_PROMPTS["default"])
        
        if template != "midjourney":  # Midjourney uses --no parameter
            prompt += f"\n\nNegative prompt: {neg_prompt}"
        else:
            prompt += f" {neg_prompt}"
    
    return prompt

class GigaPrompterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GigaPrompter 2.0 - Ultimate AI Prompt Generator")
        
        # Set window size based on platform
        if platform.system() == "Windows":
            self.root.geometry("600x800")
        else:
            self.root.geometry("500x700")
        
        # Initialize managers
        self.base_path, self.output_path, self.favorites_path, self.presets_path = CrossPlatformHelper.get_save_directory()
        self.favorites_manager = FavoritesManager(self.favorites_path)
        self.history = PromptHistory()
        self.current_prompt = None
        self.current_template = "grok_detailed"
        
        # Setup UI
        self.setup_ui()
        
        # Show platform info
        self.update_status(f"GigaPrompter 2.0 | Platform: {platform.system()} | Ready")
    
    def setup_ui(self):
        """Setup enhanced UI with all features"""
        main_container = tk.Frame(self.root, bg="#1a1a1a")
        main_container.pack(fill='both', expand=True)
        
        # Title bar
        title_frame = tk.Frame(main_container, bg="#2a2a2a", height=50)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(title_frame, text="🚀 GIGAPROMPTER 2.0", 
                              font=("Arial", 16, "bold"), fg="#00ff00", bg="#2a2a2a")
        title_label.pack(pady=10)
        
        # Top toolbar
        self.setup_toolbar(main_container)
        
        # Notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2a2a2a', borderwidth=0)
        style.configure('TNotebook.Tab', background='#3a3a3a', foreground='white', padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', '#4a4a4a')])
        
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Setup tabs
        self.quick_tab = ttk.Frame(self.notebook)
        self.advanced_tab = ttk.Frame(self.notebook)
        self.output_tab = ttk.Frame(self.notebook)
        self.batch_tab = ttk.Frame(self.notebook)
        self.favorites_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.quick_tab, text="⚡ Quick")
        self.notebook.add(self.advanced_tab, text="🔧 Advanced")
        self.notebook.add(self.output_tab, text="📝 Output")
        self.notebook.add(self.batch_tab, text="🎲 Batch")
        self.notebook.add(self.favorites_tab, text="⭐ Favorites")
        
        self.setup_quick_tab()
        self.setup_advanced_tab()
        self.setup_output_tab()
        self.setup_batch_tab()
        self.setup_favorites_tab()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_label = tk.Label(main_container, textvariable=self.status_var, 
                               bd=1, relief=tk.SUNKEN, anchor=tk.W, 
                               font=("Arial", 9), bg="#2a2a2a", fg="#00ff00")
        status_label.pack(fill=tk.X, pady=2)
    
    def setup_toolbar(self, parent):
        """Setup top toolbar with quick actions"""
        toolbar = tk.Frame(parent, bg="#2a2a2a", height=60)
        toolbar.pack(fill=tk.X, pady=(0, 5))
        
        # AI Model selector
        model_frame = tk.Frame(toolbar, bg="#2a2a2a")
        model_frame.pack(side=tk.LEFT, padx=10)
        tk.Label(model_frame, text="AI Model:", bg="#2a2a2a", fg="white", 
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        self.template_var = tk.StringVar(value="grok_detailed")
        template_combo = ttk.Combobox(model_frame, textvariable=self.template_var,
                                     values=list(AI_TEMPLATES.keys()),
                                     width=15, state="readonly", font=("Arial", 9))
        template_combo.pack(side=tk.LEFT)
        template_combo.bind("<<ComboboxSelected>>", lambda e: self.regenerate_output())
        
        # Quick preset buttons
        preset_frame = tk.Frame(toolbar, bg="#2a2a2a")
        preset_frame.pack(side=tk.LEFT, padx=20)
        tk.Label(preset_frame, text="Quick Presets:", bg="#2a2a2a", fg="white",
                font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        preset_colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57"]
        for i, preset_name in enumerate(list(PRESET_LOOKS.keys())[:5]):
            btn = tk.Button(preset_frame, text=preset_name, 
                          command=lambda p=preset_name: self.apply_preset(p),
                          font=("Arial", 8, "bold"), bg=preset_colors[i % len(preset_colors)],
                          fg="white", padx=10, pady=5, bd=0)
            btn.pack(side=tk.LEFT, padx=2)
    
    def setup_quick_tab(self):
        """Quick generation tab with essential controls"""
        main_frame = tk.Frame(self.quick_tab, bg="#2a2a2a")
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Quick randomize section
        random_frame = tk.LabelFrame(main_frame, text="🎲 Quick Random", 
                                    font=("Arial", 11, "bold"), bg="#3a3a3a", fg="white")
        random_frame.pack(fill=tk.X, pady=5)
        
        btn_frame = tk.Frame(random_frame, bg="#3a3a3a")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("🎲 Everything", self.randomize_all, "#E74C3C"),
            ("👤 Appearance", self.randomize_appearance, "#3498DB"),
            ("👗 Outfit", self.randomize_outfit, "#E67E22"),
            ("📷 Style", self.randomize_style, "#9B59B6"),
            ("✨ Attractiveness", self.randomize_attractiveness, "#1ABC9C")
        ]
        
        for text, command, color in buttons:
            tk.Button(btn_frame, text=text, command=command,
                     bg=color, fg="white", font=("Arial", 9, "bold"),
                     bd=0, padx=10, pady=8).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
        
        # Essential settings
        settings_frame = tk.LabelFrame(main_frame, text="Essential Settings", 
                                      font=("Arial", 11, "bold"), bg="#3a3a3a", fg="white")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Create grid of essential dropdowns
        essential_vars = [
            ("Age:", "age_var", VALUE_BANKS["age"]),
            ("Ethnicity:", "ethnicity_var", VALUE_BANKS["ethnicity"]),
            ("Beauty:", "beauty_var", VALUE_BANKS["beauty_level"]),
            ("Body Type:", "body_var", VALUE_BANKS["body_type"]["overall"]),
            ("Outfit:", "outfit_var", VALUE_BANKS["costume"]["main_garment"]["type"]),
            ("Setting:", "setting_var", VALUE_BANKS["background"]["setting"])
        ]
        
        for i, (label, var_name, values) in enumerate(essential_vars):
            row = i // 2
            col = i % 2
            tk.Label(settings_frame, text=label, bg="#3a3a3a", fg="white",
                    font=("Arial", 9)).grid(row=row, column=col*2, sticky="w", padx=10, pady=5)
            setattr(self, var_name, tk.StringVar())
            combo = ttk.Combobox(settings_frame, textvariable=getattr(self, var_name),
                               values=values, width=20, state="readonly")
            combo.grid(row=row, column=col*2+1, padx=5, pady=5)
        
        # Generate button
        generate_btn = tk.Button(main_frame, text="🚀 GENERATE MEGA PROMPT", 
                               command=self.generate_and_display,
                               bg="#00FF00", fg="black", font=("Arial", 12, "bold"),
                               height=3, bd=0)
        generate_btn.pack(fill=tk.X, pady=20)
    
    def setup_advanced_tab(self):
        """Advanced settings tab with all options"""
        # Create scrollable frame
        canvas = tk.Canvas(self.advanced_tab, bg="#2a2a2a")
        scrollbar = ttk.Scrollbar(self.advanced_tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set, bg="#2a2a2a")
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Attractiveness Factors Section
        attract_frame = tk.LabelFrame(scrollable_frame, text="🧬 Scientific Attractiveness Factors", 
                                     font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#00ff00")
        attract_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(attract_frame, "Facial Symmetry:", "symmetry_var", VALUE_BANKS["facial_symmetry"], 0)
        self.setup_dropdown(attract_frame, "Averageness:", "averageness_var", VALUE_BANKS["facial_averageness"], 1)
        self.setup_dropdown(attract_frame, "Skin Health:", "skin_health_var", VALUE_BANKS["skin_health"], 2)
        self.setup_dropdown(attract_frame, "Femininity:", "femininity_var", VALUE_BANKS["femininity_traits"], 3)
        self.setup_dropdown(attract_frame, "Facial Dynamics:", "dynamics_var", VALUE_BANKS["facial_dynamics"], 4)
        self.setup_dropdown(attract_frame, "Neoteny Features:", "neoteny_var", VALUE_BANKS["neoteny_features"], 5)
        self.setup_dropdown(attract_frame, "Health Indicators:", "health_var", VALUE_BANKS["health_indicators"], 6)
        
        # Physical Details Section
        phys_frame = tk.LabelFrame(scrollable_frame, text="👤 Physical Details", 
                                  font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#4ECDC4")
        phys_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(phys_frame, "Hair Color:", "hair_color_var", VALUE_BANKS["hair_color"], 0)
        self.setup_dropdown(phys_frame, "Hair Style:", "hair_style_var", VALUE_BANKS["hair_style"], 1)
        self.setup_dropdown(phys_frame, "Eye Color:", "eyes_color_var", VALUE_BANKS["eyes_color"], 2)
        self.setup_dropdown(phys_frame, "Eye Description:", "eyes_desc_var", VALUE_BANKS["eyes_description"], 3)
        self.setup_dropdown(phys_frame, "Lips:", "lips_var", VALUE_BANKS["lips_description"], 4)
        self.setup_dropdown(phys_frame, "Skin Tone:", "skin_color_var", VALUE_BANKS["skin"]["color"], 5)
        self.setup_dropdown(phys_frame, "Skin Quality:", "skin_quality_var", VALUE_BANKS["skin"]["quality"], 6)
        
        # Body Proportions Section
        body_frame = tk.LabelFrame(scrollable_frame, text="💃 Body Proportions", 
                                  font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#FF6B6B")
        body_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(body_frame, "Waist:", "waist_var", VALUE_BANKS["body_type"]["waist"], 0)
        self.setup_dropdown(body_frame, "Bust:", "bust_var", VALUE_BANKS["body_type"]["bust"], 1)
        self.setup_dropdown(body_frame, "Hips:", "hips_var", VALUE_BANKS["body_type"]["hips"], 2)
        
        # Pose & Expression Section
        pose_frame = tk.LabelFrame(scrollable_frame, text="🎭 Pose & Expression", 
                                  font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#FECA57")
        pose_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(pose_frame, "Position:", "pose_position_var", VALUE_BANKS["pose"]["position"], 0)
        self.setup_dropdown(pose_frame, "Mood:", "pose_mood_var", VALUE_BANKS["pose"]["mood"], 1)
        self.setup_dropdown(pose_frame, "Body Language:", "body_language_var", VALUE_BANKS["pose"]["body_language"], 2)
        self.setup_dropdown(pose_frame, "Hands:", "hands_var", VALUE_BANKS["pose"]["hand_placement"], 3)
        
        # Fashion Section
        fashion_frame = tk.LabelFrame(scrollable_frame, text="👗 Fashion & Style", 
                                     font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#96CEB4")
        fashion_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(fashion_frame, "Garment Type:", "garment_type_var", VALUE_BANKS["costume"]["main_garment"]["type"], 0)
        self.setup_dropdown(fashion_frame, "Style:", "garment_style_var", VALUE_BANKS["costume"]["main_garment"]["style"], 1)
        self.setup_dropdown(fashion_frame, "Color:", "garment_color_var", VALUE_BANKS["costume"]["main_garment"]["color"], 2)
        self.setup_dropdown(fashion_frame, "Material:", "material_var", VALUE_BANKS["costume"]["main_garment"]["material"], 3)
        self.setup_dropdown(fashion_frame, "Fit:", "fit_var", VALUE_BANKS["costume"]["main_garment"]["fit"], 4)
        self.setup_dropdown(fashion_frame, "Bottoms:", "bottoms_var", VALUE_BANKS["costume"]["bottoms"]["type"], 5)
        self.setup_dropdown(fashion_frame, "Footwear:", "footwear_var", VALUE_BANKS["costume"]["footwear"]["type"], 6)
        
        # Photography Settings Section
        photo_frame = tk.LabelFrame(scrollable_frame, text="📸 Photography Settings", 
                                   font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#45B7D1")
        photo_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(photo_frame, "Genre:", "genre_var", VALUE_BANKS["photo_style"]["genre"], 0)
        self.setup_dropdown(photo_frame, "Camera:", "camera_var", VALUE_BANKS["photo_style"]["camera"], 1)
        self.setup_dropdown(photo_frame, "Lens:", "lens_var", VALUE_BANKS["photo_style"]["lens"], 2)
        self.setup_dropdown(photo_frame, "Lighting:", "lighting_var", VALUE_BANKS["photo_style"]["lighting_setup"], 3)
        self.setup_dropdown(photo_frame, "Composition:", "composition_var", VALUE_BANKS["composition"]["framing"], 4)
        self.setup_dropdown(photo_frame, "Depth of Field:", "dof_var", VALUE_BANKS["composition"]["depth_of_field"], 5)
        
        # Environment Section
        env_frame = tk.LabelFrame(scrollable_frame, text="🌍 Environment", 
                                 font=("Arial", 10, "bold"), bg="#3a3a3a", fg="#E17055")
        env_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.setup_dropdown(env_frame, "Setting:", "env_setting_var", VALUE_BANKS["background"]["setting"], 0)
        self.setup_dropdown(env_frame, "Atmosphere:", "atmosphere_var", VALUE_BANKS["background"]["atmosphere"], 1)
        self.setup_dropdown(env_frame, "Time:", "time_var", VALUE_BANKS["background"]["time_of_day"], 2)
        self.setup_dropdown(env_frame, "Weather:", "weather_var", VALUE_BANKS["background"]["weather"], 3)
    
    def setup_dropdown(self, parent, label, var_name, values, row):
        """Helper to create dropdown with label"""
        tk.Label(parent, text=label, bg="#3a3a3a", fg="white", 
                font=("Arial", 9)).grid(row=row, column=0, sticky="w", padx=10, pady=4)
        setattr(self, var_name, tk.StringVar())
        combo = ttk.Combobox(parent, textvariable=getattr(self, var_name), 
                           values=values, width=35, state="readonly")
        combo.grid(row=row, column=1, padx=10, pady=4, sticky="ew")
        parent.columnconfigure(1, weight=1)
    
    def setup_output_tab(self):
        """Enhanced output tab"""
        main_frame = tk.Frame(self.output_tab, bg="#2a2a2a")
        main_frame.pack(fill='both', expand=True)
        
        # Top controls
        control_frame = tk.Frame(main_frame, bg="#3a3a3a")
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.char_count_var = tk.StringVar(value="Characters: 0")
        char_label = tk.Label(control_frame, textvariable=self.char_count_var, 
                            font=("Arial", 10, "bold"), fg="#00ff00", bg="#3a3a3a")
        char_label.pack(side=tk.LEFT, padx=10)
        
        # Options
        self.include_negative_var = tk.BooleanVar(value=True)
        tk.Checkbutton(control_frame, text="Include Negative Prompt", 
                      variable=self.include_negative_var, bg="#3a3a3a", fg="white",
                      selectcolor="#3a3a3a", font=("Arial", 9),
                      command=self.regenerate_output).pack(side=tk.LEFT, padx=10)
        
        self.format_json_var = tk.BooleanVar(value=False)
        tk.Checkbutton(control_frame, text="JSON Format", 
                      variable=self.format_json_var, bg="#3a3a3a", fg="white",
                      selectcolor="#3a3a3a", font=("Arial", 9),
                      command=self.regenerate_output).pack(side=tk.LEFT, padx=10)
        
        # Output text area
        self.output_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                    font=("Consolas", 10), bg="#1a1a1a", 
                                                    fg="#00ff00", insertbackground="#00ff00")
        self.output_text.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Button frame
        btn_frame = tk.Frame(main_frame, bg="#2a2a2a")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("📋 Copy", self.copy_to_clipboard, "#3498DB"),
            ("🔄 Regenerate", self.generate_and_display, "#E67E22"),
            ("⭐ Favorite", self.save_as_favorite, "#2ECC71"),
            ("💾 Save", self.save_to_file, "#9B59B6"),
            ("◀ Previous", self.show_previous, "#95A5A6"),
            ("▶ Next", self.show_next, "#95A5A6")
        ]
        
        for text, command, color in buttons:
            tk.Button(btn_frame, text=text, command=command,
                     bg=color, fg="white", font=("Arial", 9, "bold"),
                     bd=0, padx=10, pady=8).pack(side=tk.LEFT, padx=3, fill=tk.X, expand=True)
    
    def setup_batch_tab(self):
        """Setup batch generation tab"""
        main_frame = tk.Frame(self.batch_tab, bg="#2a2a2a")
        main_frame.pack(fill='both', expand=True)
        
        # Controls
        control_frame = tk.Frame(main_frame, bg="#3a3a3a")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(control_frame, text="Number of prompts:", bg="#3a3a3a", fg="white",
                font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
        
        self.batch_count_var = tk.IntVar(value=5)
        count_spin = tk.Spinbox(control_frame, from_=1, to=50, textvariable=self.batch_count_var, 
                               width=5, bg="#1a1a1a", fg="#00ff00", font=("Arial", 10))
        count_spin.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="🎲 Generate Batch", command=self.generate_batch,
                 bg="#2ECC71", fg="white", font=("Arial", 10, "bold"),
                 bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=20)
        
        tk.Button(control_frame, text="📋 Copy All", command=self.copy_batch,
                 bg="#3498DB", fg="white", font=("Arial", 10, "bold"),
                 bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        # Output area
        self.batch_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                   font=("Consolas", 9), bg="#1a1a1a",
                                                   fg="#00ff00", insertbackground="#00ff00")
        self.batch_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def setup_favorites_tab(self):
        """Setup favorites management tab"""
        main_frame = tk.Frame(self.favorites_tab, bg="#2a2a2a")
        main_frame.pack(fill='both', expand=True)
        
        # List frame
        list_frame = tk.Frame(main_frame, bg="#3a3a3a")
        list_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(list_frame, text="Saved Favorites:", bg="#3a3a3a", fg="white",
                font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Listbox with scrollbar
        list_container = tk.Frame(list_frame, bg="#3a3a3a")
        list_container.pack(fill=tk.X, padx=10, pady=5)
        
        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.favorites_listbox = tk.Listbox(list_container, height=8, bg="#1a1a1a", 
                                           fg="#00ff00", font=("Arial", 9),
                                           yscrollcommand=scrollbar.set)
        self.favorites_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.favorites_listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(list_frame, bg="#3a3a3a")
        btn_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("📂 Load", self.load_favorite, "#3498DB"),
            ("🗑️ Delete", self.delete_favorite, "#E74C3C"),
            ("🔄 Refresh", self.refresh_favorites, "#95A5A6")
        ]
        
        for text, command, color in buttons:
            tk.Button(btn_frame, text=text, command=command,
                     bg=color, fg="white", font=("Arial", 9, "bold"),
                     bd=0, padx=15, pady=8).pack(side=tk.LEFT, padx=5)
        
        # Preview area
        preview_frame = tk.LabelFrame(main_frame, text="Preview", 
                                     font=("Arial", 10, "bold"), bg="#3a3a3a", fg="white")
        preview_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.favorites_preview = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, 
                                                          font=("Consolas", 9), height=10,
                                                          bg="#1a1a1a", fg="#00ff00")
        self.favorites_preview.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Load initial favorites
        self.refresh_favorites()
    
    def randomize_all(self):
        """Randomize all settings"""
        # Clear all variables to trigger random selection
        for attr_name in dir(self):
            if attr_name.endswith('_var'):
                var = getattr(self, attr_name, None)
                if var and hasattr(var, 'set'):
                    # Check the type of variable and set appropriate default
                    if isinstance(var, tk.BooleanVar):
                        # For boolean variables, randomly set True or False
                        var.set(random.choice([True, False]))
                    elif isinstance(var, tk.IntVar):
                        # For integer variables, keep current value or set default
                        continue  # Skip IntVars (like batch_count_var)
                    elif isinstance(var, tk.StringVar):
                        # For string variables, set empty to trigger random selection
                        var.set("")
                    else:
                        # For any other type, try setting empty string
                        try:
                            var.set("")
                        except:
                            pass  # Skip if it fails
        self.update_status("✓ Randomized all settings")
    
    def randomize_appearance(self):
        """Randomize physical appearance"""
        # Safely set each variable if it exists
        vars_to_randomize = {
            'age_var': VALUE_BANKS["age"],
            'ethnicity_var': VALUE_BANKS["ethnicity"],
            'beauty_var': VALUE_BANKS["beauty_level"],
            'hair_color_var': VALUE_BANKS["hair_color"],
            'hair_style_var': VALUE_BANKS["hair_style"],
            'eyes_color_var': VALUE_BANKS["eyes_color"],
            'eyes_desc_var': VALUE_BANKS["eyes_description"],
            'lips_var': VALUE_BANKS["lips_description"],
            'skin_color_var': VALUE_BANKS["skin"]["color"],
            'skin_quality_var': VALUE_BANKS["skin"]["quality"],
            'bust_var': VALUE_BANKS["body_type"]["bust"],
            'waist_var': VALUE_BANKS["body_type"]["waist"],
            'hips_var': VALUE_BANKS["body_type"]["hips"],
            'body_var': VALUE_BANKS["body_type"]["overall"]
        }
        
        for var_name, values in vars_to_randomize.items():
            if hasattr(self, var_name):
                var = getattr(self, var_name)
                if hasattr(var, 'set'):
                    var.set(random.choice(values))
        
        self.update_status("✓ Randomized appearance")
    
    def randomize_outfit(self):
        """Randomize outfit"""
        vars_to_randomize = {
            'outfit_var': VALUE_BANKS["costume"]["main_garment"]["type"],
            'garment_type_var': VALUE_BANKS["costume"]["main_garment"]["type"],
            'garment_style_var': VALUE_BANKS["costume"]["main_garment"]["style"],
            'garment_color_var': VALUE_BANKS["costume"]["main_garment"]["color"],
            'material_var': VALUE_BANKS["costume"]["main_garment"]["material"],
            'fit_var': VALUE_BANKS["costume"]["main_garment"]["fit"],
            'bottoms_var': VALUE_BANKS["costume"]["bottoms"]["type"],
            'footwear_var': VALUE_BANKS["costume"]["footwear"]["type"]
        }
        
        for var_name, values in vars_to_randomize.items():
            if hasattr(self, var_name):
                var = getattr(self, var_name)
                if hasattr(var, 'set'):
                    var.set(random.choice(values))
        
        self.update_status("✓ Randomized outfit")
    
    def randomize_style(self):
        """Randomize photo style and background"""
        vars_to_randomize = {
            'setting_var': VALUE_BANKS["background"]["setting"],
            'env_setting_var': VALUE_BANKS["background"]["setting"],
            'atmosphere_var': VALUE_BANKS["background"]["atmosphere"],
            'time_var': VALUE_BANKS["background"]["time_of_day"],
            'weather_var': VALUE_BANKS["background"]["weather"],
            'genre_var': VALUE_BANKS["photo_style"]["genre"],
            'camera_var': VALUE_BANKS["photo_style"]["camera"],
            'lens_var': VALUE_BANKS["photo_style"]["lens"],
            'lighting_var': VALUE_BANKS["photo_style"]["lighting_setup"],
            'composition_var': VALUE_BANKS["composition"]["framing"],
            'dof_var': VALUE_BANKS["composition"]["depth_of_field"]
        }
        
        for var_name, values in vars_to_randomize.items():
            if hasattr(self, var_name):
                var = getattr(self, var_name)
                if hasattr(var, 'set'):
                    var.set(random.choice(values))
        
        self.update_status("✓ Randomized style")
    
    def randomize_attractiveness(self):
        """Randomize attractiveness factors"""
        vars_to_randomize = {
            'symmetry_var': VALUE_BANKS["facial_symmetry"],
            'averageness_var': VALUE_BANKS["facial_averageness"],
            'skin_health_var': VALUE_BANKS["skin_health"],
            'femininity_var': VALUE_BANKS["femininity_traits"],
            'dynamics_var': VALUE_BANKS["facial_dynamics"],
            'neoteny_var': VALUE_BANKS["neoteny_features"],
            'health_var': VALUE_BANKS["health_indicators"]
        }
        
        for var_name, values in vars_to_randomize.items():
            if hasattr(self, var_name):
                var = getattr(self, var_name)
                if hasattr(var, 'set'):
                    var.set(random.choice(values))
        
        self.update_status("✓ Randomized attractiveness factors")
    
    def apply_preset(self, preset_name):
        """Apply a preset look"""
        if preset_name not in PRESET_LOOKS:
            return
        
        preset = PRESET_LOOKS[preset_name]
        
        # Map preset keys to variable names
        var_map = {
            'beauty_level': 'beauty_var',
            'facial_symmetry': 'symmetry_var',
            'facial_averageness': 'averageness_var',
            'skin_health': 'skin_health_var',
            'facial_dynamics': 'dynamics_var',
            'photo_quality': 'quality_var',
            'style_reference': 'style_var',
            'pose_mood': 'pose_mood_var',
            'background_atmosphere': 'atmosphere_var',
            'character': 'character_var',
            'main_garment_type': 'outfit_var',
            'background_setting': 'setting_var',
            'hair_style': 'hair_style_var',
            'skin_quality': 'skin_quality_var',
            'body_overall': 'body_var',
            'lighting_type': 'lighting_var',
            'composition_framing': 'composition_var',
            'neoteny': 'neoteny_var',
            'health_indicators': 'health_var',
            'femininity_traits': 'femininity_var'
        }
        
        for key, value in preset.items():
            var_name = var_map.get(key, key + '_var')
            if hasattr(self, var_name):
                getattr(self, var_name).set(value)
        
        self.update_status(f"✓ Applied preset: {preset_name}")
    
    def generate_and_display(self):
        """Generate and display AI-optimized prompt"""
        try:
            # Collect custom values from UI
            custom_values = {}
            
            # Collect all variables that have been set
            for attr_name in dir(self):
                if attr_name.endswith('_var'):
                    var = getattr(self, attr_name, None)
                    if var and hasattr(var, 'get'):
                        value = var.get()
                        if value:
                            # Map variable names to prompt keys
                            key = attr_name.replace('_var', '')
                            if attr_name == 'age_var':
                                custom_values['age'] = int(value)
                            else:
                                custom_values[key] = value
            
            # Generate prompt
            self.current_prompt = generate_prompt(custom_values=custom_values)
            
            # Create AI-optimized output
            template = self.template_var.get()
            
            if self.format_json_var.get():
                # JSON format
                plain_text = json.dumps(self.current_prompt, indent=2)
            else:
                # Text format
                plain_text = create_ai_optimized_prompt(
                    self.current_prompt, 
                    template, 
                    self.include_negative_var.get()
                )
            
            # Display
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, plain_text)
            self.update_char_count()
            
            # Add to history
            self.history.add(self.current_prompt, plain_text)
            
            # Switch to output tab
            self.notebook.select(self.output_tab)
            
            model_name = template.split('_')[0].upper()
            self.update_status(f"✓ Generated {model_name} prompt - {len(plain_text)} chars")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate: {str(e)}")
            self.update_status(f"✗ Error: {str(e)}")
    
    def regenerate_output(self):
        """Regenerate output with current settings"""
        if self.current_prompt:
            template = self.template_var.get()
            
            if self.format_json_var.get():
                plain_text = json.dumps(self.current_prompt, indent=2)
            else:
                plain_text = create_ai_optimized_prompt(
                    self.current_prompt,
                    template,
                    self.include_negative_var.get()
                )
            
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, plain_text)
            self.update_char_count()
    
    def generate_batch(self):
        """Generate multiple prompts"""
        count = self.batch_count_var.get()
        self.batch_text.delete(1.0, tk.END)
        
        template = self.template_var.get()
        include_negative = self.include_negative_var.get()
        
        for i in range(count):
            prompt = generate_prompt()
            plain_text = create_ai_optimized_prompt(prompt, template, include_negative)
            
            self.batch_text.insert(tk.END, f"━━━ PROMPT {i+1} ━━━\n")
            self.batch_text.insert(tk.END, plain_text + "\n\n")
        
        self.update_status(f"✓ Generated {count} prompts for {template.split('_')[0].upper()}")
    
    def copy_batch(self):
        """Copy all batch prompts"""
        text = self.batch_text.get(1.0, tk.END).strip()
        if text:
            success, method = CrossPlatformHelper.copy_to_clipboard(text, self.root)
            if success:
                self.update_status(f"✓ Copied batch ({method})")
            else:
                self.update_status("✗ Copy failed")
    
    def save_as_favorite(self):
        """Save current prompt as favorite"""
        if not self.current_prompt:
            messagebox.showwarning("No Prompt", "Generate a prompt first")
            return
        
        # Create custom dialog for name input
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Favorite")
        dialog.geometry("300x100")
        dialog.configure(bg="#2a2a2a")
        
        tk.Label(dialog, text="Enter name for this favorite:", 
                bg="#2a2a2a", fg="white", font=("Arial", 10)).pack(pady=10)
        
        name_var = tk.StringVar()
        entry = tk.Entry(dialog, textvariable=name_var, bg="#1a1a1a", 
                        fg="#00ff00", font=("Arial", 10))
        entry.pack(pady=5, padx=20, fill=tk.X)
        entry.focus()
        
        def save():
            name = name_var.get()
            if name:
                plain_text = self.output_text.get(1.0, tk.END).strip()
                if self.favorites_manager.save_favorite(name, self.current_prompt, plain_text):
                    self.update_status(f"✓ Saved as '{name}'")
                    self.refresh_favorites()
                dialog.destroy()
        
        tk.Button(dialog, text="Save", command=save, bg="#2ECC71", 
                 fg="white", font=("Arial", 9, "bold"), bd=0,
                 padx=20, pady=5).pack(pady=10)
        
        entry.bind('<Return>', lambda e: save())
    
    def refresh_favorites(self):
        """Refresh favorites list"""
        self.favorites_listbox.delete(0, tk.END)
        for name in self.favorites_manager.get_favorite_names():
            self.favorites_listbox.insert(tk.END, name)
        
        # Bind selection event
        self.favorites_listbox.bind('<<ListboxSelect>>', self.preview_favorite)
    
    def preview_favorite(self, event=None):
        """Preview selected favorite"""
        selection = self.favorites_listbox.curselection()
        if selection:
            name = self.favorites_listbox.get(selection[0])
            favorite = self.favorites_manager.load_favorite(name)
            if favorite:
                self.favorites_preview.delete(1.0, tk.END)
                self.favorites_preview.insert(tk.END, favorite['plain_text'])
    
    def load_favorite(self):
        """Load selected favorite"""
        selection = self.favorites_listbox.curselection()
        if selection:
            name = self.favorites_listbox.get(selection[0])
            favorite = self.favorites_manager.load_favorite(name)
            if favorite:
                self.current_prompt = favorite['prompt']
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, favorite['plain_text'])
                self.notebook.select(self.output_tab)
                self.update_status(f"✓ Loaded '{name}'")
    
    def delete_favorite(self):
        """Delete selected favorite"""
        selection = self.favorites_listbox.curselection()
        if selection:
            name = self.favorites_listbox.get(selection[0])
            if messagebox.askyesno("Delete Favorite", f"Delete '{name}'?"):
                self.favorites_manager.delete_favorite(name)
                self.refresh_favorites()
                self.update_status(f"✓ Deleted '{name}'")
    
    def show_previous(self):
        """Show previous prompt from history"""
        entry = self.history.get_previous()
        if entry:
            self.current_prompt = entry['prompt']
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, entry['plain_text'])
            self.update_char_count()
    
    def show_next(self):
        """Show next prompt from history"""
        entry = self.history.get_next()
        if entry:
            self.current_prompt = entry['prompt']
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, entry['plain_text'])
            self.update_char_count()
    
    def copy_to_clipboard(self):
        """Cross-platform clipboard copy"""
        text = self.output_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("No Content", "No prompt to copy")
            return
        
        success, method = CrossPlatformHelper.copy_to_clipboard(text, self.root)
        if success:
            self.update_status(f"✓ Copied {len(text)} chars ({method})")
        else:
            self.output_text.tag_add(tk.SEL, "1.0", tk.END)
            self.output_text.focus_set()
            self.update_status("Text selected - use Ctrl+C")
    
    def save_to_file(self):
        """Save to file"""
        text = self.output_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("No Content", "No prompt to save")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            template = self.template_var.get()
            default_filename = f"gigaprompt_{template}_{timestamp}.txt"
            
            file_path = filedialog.asksaveasfilename(
                initialdir=str(self.output_path),
                initialfile=default_filename,
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(f"# GigaPrompter 2.0 Output\n")
                    f.write(f"# Template: {template}\n")
                    f.write(f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"# Platform: {platform.system()}\n\n")
                    f.write(text)
                
                self.update_status(f"✓ Saved to {Path(file_path).name}")
        
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save: {str(e)}")
    
    def update_char_count(self, event=None):
        """Update character count"""
        text = self.output_text.get(1.0, tk.END).strip()
        char_count = len(text)
        
        # Color code based on length for different AI models
        if char_count <= 500:
            color = "#2ECC71"  # Green
            status = "✓ Optimal"
        elif char_count <= 1000:
            color = "#F39C12"  # Orange
            status = "⚠ Long"
        elif char_count <= 2000:
            color = "#E67E22"  # Dark Orange
            status = "⚠ Very Long"
        else:
            color = "#E74C3C"  # Red
            status = "⚠ Excessive"
        
        self.char_count_var.set(f"Characters: {char_count} {status}")
    
    def update_status(self, message):
        """Update status bar with auto-clear"""
        self.status_var.set(message)
        # Auto-clear after 5 seconds
        self.root.after(5000, lambda: self.status_var.set("GigaPrompter 2.0 Ready"))


def main():
    """Main entry point"""
    try:
        # Import tkinter simpledialog if missing
        import tkinter.simpledialog as simpledialog
        tk.simpledialog = simpledialog
    except:
        pass
    
    # Create main window
    root = tk.Tk()
    
    # Set icon if available (Windows)
    if platform.system() == "Windows":
        try:
            root.iconbitmap(default='icon.ico')
        except:
            pass
    
    # Configure style
    root.configure(bg="#1a1a1a")
    
    # Initialize application
    app = GigaPrompterApp(root)
    
    # Center window on screen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    # Run main loop
    root.mainloop()


if __name__ == "__main__":
    main()