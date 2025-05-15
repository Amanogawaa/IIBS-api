from better_profanity import profanity
import re
import os
import json

class ProfanityFilter:
    def __init__(self, load_tagalog=True):
        # Initialize the profanity filter
        self.profanity = profanity
        
        # Load default English profanity words
        self.profanity.load_censor_words()
        
        # Add Tagalog profanity words if requested
        if load_tagalog:
            self._load_tagalog_profanity()
            
        # Add additional Tagalog profanity words that might not be in the dataset
        self._add_additional_tagalog_profanity()
    
    def _load_tagalog_profanity(self):
        """Load Tagalog profanity words from a local file or create the file if it doesn't exist"""
        file_path = os.path.join(os.path.dirname(__file__), "tagalog_profanity.json")
        
        try:
            # Try to load from local file first (faster and doesn't require internet connection)
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    tagalog_words = json.load(f)
                    self.profanity.add_censor_words(tagalog_words)
            else:
                # If file doesn't exist, load from Hugging Face dataset
                try:
                    from datasets import load_dataset
                    ds = load_dataset("mginoben/tagalog-profanity-dataset")
                    
                    tagalog_words = []
                    for example in ds['train']:
                        word = example['text']
                        tagalog_words.append(word.lower())
                    
                    # Save to local file for future use
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(tagalog_words, f, ensure_ascii=False)
                    
                    self.profanity.add_censor_words(tagalog_words)
                except Exception as e:
                    print(f"Warning: Could not load Tagalog profanity dataset: {e}")
        except Exception as e:
            print(f"Warning: Error loading profanity list: {e}")
            
    def _add_additional_tagalog_profanity(self):
        """Add additional common Tagalog profanity words and phrases that might not be in the dataset"""
        # Common Tagalog profanity words and their variations
        additional_words = [
            # Basic profanity words
            "puta", "putang", "putangina", "putanginamo", "putragis", "pota", "potangina",
            "gago", "gaga", "gagawin", "pakyu", "pak yu", "pakyo", "ulol", "ulul", "tanga",
            "tae", "taena", "tainga", "hinayupak", "hayop", "hayupak", "leche", "lecheng",
            
            # Sexual terms
            "burat", "buratmo", "burnik", "kantot", "kantutan", "iyot", "iyutan", "jakol",
            "titi", "titimo", "pepe", "pepemo", "maliit", "bayag", "bayagmo", "bayagmong", 
            "burat mo", "buratmo", "kantot mo", "kantotmo", "iyot mo", "iyotmo",
            "titi mo", "titimo", "pepe mo", "pepemo", "bayag mo", "bayagmo",
            
            # Combined phrases
            "burat mo maliit", "maliit ang burat mo", "burat mong maliit",
            "titi mo maliit", "maliit ang titi mo", "titi mong maliit",
            
            # Insults
            "bobo", "boboka", "bobomo", "bobong", "tanga", "tangamo", "tangaka", "tangina",
            "tanginamo", "inamo", "putanginamo", "hindot", "hindutan", "ogag", "gagi",
            "pucha", "kupal", "kupalmo", "kupalka", "tarantado", "tarantadoka", "siraulo",
            "anak ng puta", "anakniputa", "anakngputangina",
            
            # Variations with spaces
            "puta mo", "putang ina", "putang ina mo", "tang ina", "tang ina mo",
            "gago ka", "tanga ka", "tae mo", "taena mo", "hayop ka", "leche ka",
            "bobo ka", "tanga ka", "tangina mo", "ina mo", "putangina mo",
            
            # Common misspellings and variations
            "p*ta", "p*tangina", "g*go", "t*ngina", "f*ck", "p*kyu", "puñeta"
        ]
        
        self.profanity.add_censor_words(additional_words)
    
    def contains_profanity(self, text):
        """Check if text contains profanity"""
        return self.profanity.contains_profanity(text)
    
    def censor(self, text):
        """Censor profanity in text"""
        return self.profanity.censor(text)
        
    def add_words(self, words):
        """Add new profanity words to the filter"""
        if isinstance(words, str):
            words = [words]
        self.profanity.add_censor_words(words)
        
    def add_and_save_words(self, words):
        """Add new profanity words and save them to the local file"""
        if isinstance(words, str):
            words = [words]
            
        self.profanity.add_censor_words(words)
        
        # Update the local file if it exists
        file_path = os.path.join(os.path.dirname(__file__), "tagalog_profanity.json")
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    existing_words = json.load(f)
                
                # Add new words
                existing_words.extend([w for w in words if w not in existing_words])
                
                # Save back to file
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(existing_words, f, ensure_ascii=False)
            except Exception as e:
                print(f"Warning: Could not update profanity file: {e}")

def is_meaningful_text(text: str, min_chars=5, min_words=3, max_non_alpha_ratio=0.5) -> bool:
    """
    Enhanced validation for text to ensure it's meaningful:
    - Minimum character length (default: 5)
    - Minimum word count (default: 3)
    - Contains at least one letter
    - No excessive punctuation (less than 50% non-alphabetic by default)
    - No profanity (using better-profanity with Tagalog dataset)
    
    Returns True if text is meaningful, False otherwise
    """
    if not text or len(text.strip()) < min_chars:
        return False
    
    # Strip and normalize text
    normalized_text = text.strip().lower()
    
    # Split into words and check minimum word count
    words = normalized_text.split()
    if len(words) < min_words:
        return False
    
    # Check for at least one letter
    if not any(c.isalpha() for c in normalized_text):
        return False
    
    # Check for excessive punctuation or special characters
    non_alpha = sum(1 for c in normalized_text if not c.isalpha() and not c.isspace())
    if non_alpha / len(normalized_text) > max_non_alpha_ratio:
        return False
    
    # Check for profanity - using singleton pattern
    global _profanity_filter
    if '_profanity_filter' not in globals():
        _profanity_filter = ProfanityFilter()
    
    # Check whole text for profanity
    if _profanity_filter.contains_profanity(normalized_text):
        return False
    
    # Also check individual words and common phrase combinations
    for i in range(len(words)):
        # Check single words
        if _profanity_filter.contains_profanity(words[i]):
            return False
        
        # Check pairs of words (useful for catching phrases like "burat mo")
        if i < len(words) - 1:
            phrase = words[i] + " " + words[i+1]
            if _profanity_filter.contains_profanity(phrase):
                return False
        
        # Check triplets of words
        if i < len(words) - 2:
            phrase = words[i] + " " + words[i+1] + " " + words[i+2]
            if _profanity_filter.contains_profanity(phrase):
                return False
    
    return True