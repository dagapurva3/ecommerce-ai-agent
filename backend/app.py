"""
Commerce AI Agent - Main Flask Application
A comprehensive AI-powered shopping assistant with conversation, recommendations, and image search capabilities.
Inspired by Amazon's Rufus, this application provides intelligent product discovery and customer assistance.
"""

import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from product_catalog import ProductCatalog
from nlp_utils import process_query, process_image_description
import os
import logging
from datetime import datetime
from dotenv import load_dotenv
import random
import requests

# NLTK Setup - Download required data
import nltk

try:
    # Try to download required NLTK data
    nltk.download("punkt_tab", quiet=True)
    nltk.download("punkt", quiet=True)  # Backup for older versions
    nltk.download("stopwords", quiet=True)
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
except Exception as e:
    print(f"Warning: Could not download NLTK data: {e}")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend
load_dotenv()

# Initialize product catalog
catalog = ProductCatalog()

# Initialize Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint for the API."""
    return jsonify(
        {
            "status": "healthy",
            "message": "Commerce AI Agent API is running",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Handle general conversation with the AI agent.

    Expected request body:
    {
        "query": "string" - The user's message
    }

    Returns:
    {
        "response": "string" - AI agent's response
        "timestamp": "string" - Response timestamp
        "products": [array] - (optional) List of recommended products
    }
    """
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Query is required"}), 400

        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400

        logger.info(f"Processing chat query: {query}")

        # Process query using NLP
        response = process_query(query)

        # Try to get product recommendations for this query
        recommendations = catalog.recommend_products(query)
        # logger.info(recommendations)
        result = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
        }
        if recommendations:
            result["products"] = recommendations

        return jsonify(result)

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/recommend", methods=["POST"])
def recommend():
    """
    Provide text-based product recommendations.

    Expected request body:
    {
        "query": "string" - Product search query
    }

    Returns:
    {
        "products": [array] - List of recommended products
        "query": "string" - Original query
        "count": "int" - Number of recommendations
    }
    """
    try:
        data = request.get_json()
        if not data or "query" not in data:
            return jsonify({"error": "Query is required"}), 400

        query = data.get("query", "").strip()
        if not query:
            return jsonify({"error": "Query cannot be empty"}), 400

        logger.info(f"Processing recommendation query: {query}")

        # Get recommendations from catalog
        recommendations = catalog.recommend_products(query)

        return jsonify(
            {
                "products": recommendations,
                "query": query,
                "count": len(recommendations),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/image_search", methods=["POST"])
def image_search():
    """
    Simulate image-based product search using description.

    Expected request body:
    {
        "description": "string" - Image description
    }

    Returns:
    {
        "products": [array] - List of matching products
        "description": "string" - Original description
        "count": "int" - Number of matches
    }
    """
    try:
        data = request.get_json()
        if not data or "description" not in data:
            return jsonify({"error": "Description is required"}), 400

        description = data.get("description", "").strip()
        if not description:
            return jsonify({"error": "Description cannot be empty"}), 400

        logger.info(f"Processing image search: {description}")

        # Process image description and find matching products
        recommendations = process_image_description(description, catalog)

        return jsonify(
            {
                "products": recommendations,
                "description": description,
                "count": len(recommendations),
                "timestamp": datetime.now().isoformat(),
            }
        )

    except Exception as e:
        logger.error(f"Error in image_search endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/products", methods=["GET"])
def get_all_products():
    """
    Get all available products in the catalog.

    Returns:
    {
        "products": [array] - All products
        "count": "int" - Total number of products
    }
    """
    try:
        all_products = catalog.get_all_products()
        return jsonify(
            {
                "products": all_products,
                "count": len(all_products),
                "timestamp": datetime.now().isoformat(),
            }
        )
    except Exception as e:
        logger.error(f"Error in get_all_products endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/image_upload", methods=["POST"])
def image_upload():
    """
    Simulate image-based product search using uploaded image.
    """
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files["image"]
    filename = image.filename.lower()

    # Simulate object detection by using keywords in the filename
    keywords = filename.replace(".", " ").replace("_", " ").split()
    all_products = catalog.get_all_products()
    matches = []
    for product in all_products:
        product_text = f"{product['name']} {product['description']}".lower()
        if any(word in product_text for word in keywords):
            matches.append(product)
    if not matches:
        matches = random.sample(all_products, min(3, len(all_products)))
    return jsonify({"products": matches})


@app.route("/api/agent_chat", methods=["POST"])
def agent_chat():
    data = request.get_json()
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Query required"}), 400
    try:
        gemini_response = gemini_text(query)
        # Get product recommendations from the catalog using the Gemini response
        recommendations = catalog.recommend_products(gemini_response)
        result = {
            "response": gemini_response,
            "timestamp": datetime.now().isoformat(),
        }
        # logger.info(recommendations)
        if recommendations:
            result["products"] = recommendations
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in agent_chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/agent_image", methods=["POST"])
def agent_image():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    image = request.files["image"]
    image_bytes = image.read()
    prompt = request.form.get("prompt", "What products do you see?")
    try:
        gemini_response = gemini_vision(image_bytes, prompt)
        return jsonify({"response": gemini_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({"error": "Internal server error"}), 500


def gemini_text(prompt):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    response = requests.post(url, headers=headers, params=params, json=data)
    logger.info(response.json())
    response.raise_for_status()
    return response.json()["candidates"][0]["content"]["parts"][0]["text"]


def gemini_vision(image_bytes, prompt="What do you see?", mime_type="image/jpeg"):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    data = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": mime_type, "data": image_b64}},
                ],
            }
        ]
    }

    response = requests.post(url, headers=headers, params=params, json=data)

    try:
        response.raise_for_status()
        res_json = response.json()
        logger.info("Gemini response: %s", res_json)

        return res_json["candidates"][0]["content"]["parts"][0]["text"]

    except requests.exceptions.RequestException as e:
        logger.error("Request failed: %s", e)
        raise

    except (KeyError, IndexError) as e:
        logger.error("Unexpected response structure: %s", response.text)
        raise RuntimeError("Unexpected response structure from Gemini API") from e


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("DEBUG", "True").lower() == "true"

    logger.info(f"Starting Commerce AI Agent on port {port}")
    app.run(debug=debug, host="0.0.0.0", port=port)
