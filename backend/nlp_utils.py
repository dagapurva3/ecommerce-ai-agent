"""
Natural Language Processing Utilities for Commerce AI Agent
Handles query processing, intent recognition, and semantic matching for product recommendations.
"""

import re
import string
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import logging

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

logger = logging.getLogger(__name__)


class NLPProcessor:
    """Natural Language Processing processor for commerce queries."""

    def __init__(self):
        """Initialize NLP processor with required components."""
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(
            max_features=1000, stop_words="english", ngram_range=(1, 2)
        )

        # Define conversation patterns
        self.conversation_patterns = {
            "greeting": [
                r"\b(hi|hello|hey|good morning|good afternoon|good evening)\b",
                r"\b(how are you|how\'s it going)\b",
            ],
            "identity": [
                r"\b(what\'s your name|who are you|what do you call yourself)\b",
                r"\b(are you a bot|are you ai|are you artificial intelligence)\b",
            ],
            "capabilities": [
                r"\b(what can you do|what are your features|help|what do you offer)\b",
                r"\b(how do you work|how can you help me)\b",
            ],
            "thanks": [r"\b(thank you|thanks|thx|appreciate it)\b"],
            "goodbye": [r"\b(bye|goodbye|see you|farewell|exit|quit)\b"],
        }

        # Define product categories and keywords
        self.product_categories = {
            "clothing": [
                "shirt",
                "t-shirt",
                "pants",
                "jeans",
                "dress",
                "sweater",
                "jacket",
                "coat",
                "shoes",
                "sneakers",
                "boots",
            ],
            "sports": [
                "sports",
                "athletic",
                "running",
                "gym",
                "workout",
                "exercise",
                "fitness",
            ],
            "electronics": [
                "phone",
                "laptop",
                "computer",
                "tablet",
                "headphones",
                "camera",
                "tv",
            ],
            "home": ["furniture", "chair", "table", "bed", "lamp", "decor", "kitchen"],
            "books": ["book", "novel", "textbook", "magazine", "journal"],
        }

    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text by cleaning and normalizing.

        Args:
            text (str): Input text to preprocess

        Returns:
            str: Preprocessed text
        """
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove punctuation
        text = text.translate(str.maketrans("", "", string.punctuation))

        # Tokenize
        tokens = word_tokenize(text)

        # Remove stop words and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]

        return " ".join(tokens)

    def detect_intent(self, query: str) -> str:
        """
        Detect the intent of a user query.

        Args:
            query (str): User's query

        Returns:
            str: Detected intent (greeting, identity, capabilities, thanks, goodbye, product_search)
        """
        query_lower = query.lower()

        # Check conversation patterns
        for intent, patterns in self.conversation_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower):
                    return intent

        # Check for product-related keywords
        product_keywords = [
            "recommend",
            "search",
            "find",
            "show",
            "buy",
            "purchase",
            "looking for",
            "need",
        ]
        if any(keyword in query_lower for keyword in product_keywords):
            return "product_search"

        return "general"

    def extract_product_features(self, query: str) -> Dict[str, Any]:
        """
        Extract product features from a query.

        Args:
            query (str): Product search query

        Returns:
            Dict[str, Any]: Extracted features
        """
        query_lower = query.lower()
        features = {
            "category": None,
            "attributes": [],
            "price_range": None,
            "brand": None,
        }

        # Extract category
        for category, keywords in self.product_categories.items():
            if any(keyword in query_lower for keyword in keywords):
                features["category"] = category
                break

        # Extract attributes (color, size, material, etc.)
        color_keywords = [
            "red",
            "blue",
            "green",
            "black",
            "white",
            "yellow",
            "purple",
            "pink",
            "brown",
            "gray",
            "grey",
        ]
        size_keywords = ["small", "medium", "large", "xl", "xxl", "xs"]
        material_keywords = ["cotton", "polyester", "leather", "wool", "silk", "denim"]

        for color in color_keywords:
            if color in query_lower:
                features["attributes"].append(f"color:{color}")

        for size in size_keywords:
            if size in query_lower:
                features["attributes"].append(f"size:{size}")

        for material in material_keywords:
            if material in query_lower:
                features["attributes"].append(f"material:{material}")

        return features


def process_query(query: str) -> str:
    """
    Process a general conversation query and return an appropriate response.

    Args:
        query (str): User's query

    Returns:
        str: AI agent's response
    """
    processor = NLPProcessor()
    intent = processor.detect_intent(query)

    responses = {
        "greeting": [
            "Hello! I'm your AI shopping assistant. How can I help you today?",
            "Hi there! I'm here to help you find the perfect products. What are you looking for?",
            "Greetings! I'm your personal shopping companion. How may I assist you?",
        ],
        "identity": [
            "I'm ShopBot, your AI-powered shopping assistant! I can help you find products, make recommendations, and answer questions about our catalog.",
            "My name is ShopBot! I'm an AI agent designed to make your shopping experience easier and more enjoyable.",
            "I'm ShopBot, your intelligent shopping companion. I can search products, provide recommendations, and help you make informed decisions.",
        ],
        "capabilities": [
            "I can help you with:\n• Product recommendations based on your needs\n• Searching for specific items\n• Answering questions about products\n• Simulating image-based searches\n• General shopping assistance\n\nJust tell me what you're looking for!",
            "Here's what I can do for you:\n• Find products that match your requirements\n• Recommend items based on your preferences\n• Help you discover new products\n• Answer questions about our catalog\n• Assist with your shopping decisions\n\nWhat would you like to explore?",
            "My capabilities include:\n• Intelligent product search and recommendations\n• Natural conversation about shopping\n• Image-based product discovery (simulated)\n• Personalized shopping assistance\n• Product information and details\n\nHow can I help you today?",
        ],
        "thanks": [
            "You're welcome! I'm happy to help. Is there anything else you'd like to know?",
            "My pleasure! Feel free to ask if you need any more assistance.",
            "Glad I could help! Don't hesitate to reach out if you have more questions.",
        ],
        "goodbye": [
            "Goodbye! Happy shopping! Come back anytime you need assistance.",
            "See you later! I hope you found what you were looking for.",
            "Take care! I'll be here when you need shopping help again.",
        ],
        "product_search": [
            "I'd be happy to help you find products! Could you tell me more specifically what you're looking for?",
            "Great! I can help you discover the perfect products. What type of item are you interested in?",
            "Perfect! I'm here to help you find exactly what you need. What are you searching for?",
        ],
        "general": [
            "I'm here to help with your shopping needs! You can ask me to recommend products, search for specific items, or just chat about shopping.",
            "I'm your shopping assistant! Feel free to ask me about products, recommendations, or any shopping-related questions.",
            "I'm here to make your shopping experience better! What would you like to know about our products?",
        ],
    }

    import random

    return random.choice(responses.get(intent, responses["general"]))


def process_image_description(description: str, catalog) -> List[Dict[str, Any]]:
    """
    Process an image description and find matching products.

    Args:
        description (str): Description of the image
        catalog: Product catalog instance

    Returns:
        List[Dict[str, Any]]: List of matching products
    """
    processor = NLPProcessor()

    # Preprocess the description
    processed_desc = processor.preprocess_text(description)

    # Extract features from description
    features = processor.extract_product_features(description)

    # Get all products
    all_products = catalog.get_all_products()

    if not all_products:
        return []

    # Create product descriptions for comparison
    product_descriptions = []
    for product in all_products:
        product_text = f"{product['name']} {product['description']}"
        if features["category"]:
            product_text += f" {features['category']}"
        product_descriptions.append(processor.preprocess_text(product_text))

    # Vectorize descriptions
    try:
        all_texts = [processed_desc] + product_descriptions
        tfidf_matrix = processor.vectorizer.fit_transform(all_texts)

        # Calculate similarities
        similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

        # Get top matches
        top_indices = similarities[0].argsort()[-5:][::-1]  # Top 5 matches

        matches = []
        for idx in top_indices:
            if similarities[0][idx] > 0.1:  # Minimum similarity threshold
                matches.append(all_products[idx])

        return matches

    except Exception as e:
        logger.error(f"Error in image description processing: {str(e)}")
        # Fallback: return products based on keyword matching
        matches = []
        for product in all_products:
            product_text = f"{product['name']} {product['description']}".lower()
            if any(word in product_text for word in description.lower().split()):
                matches.append(product)

        return matches[:5]  # Return top 5 matches
