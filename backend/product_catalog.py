"""
Product Catalog Management for Commerce AI Agent
Handles product storage, retrieval, and recommendation logic.
"""

import json
import os
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)


class ProductCatalog:
    """Manages product catalog operations including search and recommendations."""

    def __init__(self, catalog_file: str = "products.json"):
        """
        Initialize the product catalog.

        Args:
            catalog_file (str): Path to the JSON file containing products
        """
        self.catalog_file = catalog_file
        self.products = []
        self.vectorizer = TfidfVectorizer(
            max_features=1000, stop_words="english", ngram_range=(1, 2)
        )
        self.load_products()

    def load_products(self) -> None:
        """Load products from the JSON file."""
        try:
            if os.path.exists(self.catalog_file):
                with open(self.catalog_file, "r", encoding="utf-8") as f:
                    self.products = json.load(f)
                logger.info(f"Loaded {len(self.products)} products from catalog")
            else:
                logger.warning(
                    f"Catalog file {self.catalog_file} not found. Creating sample catalog."
                )
                self.create_sample_catalog()
        except Exception as e:
            logger.error(f"Error loading products: {str(e)}")
            self.create_sample_catalog()

    def create_sample_catalog(self) -> None:
        """Create a sample product catalog with diverse products."""
        sample_products = [
            {
                "id": 1,
                "name": "Nike Air Max Running Shoes",
                "description": "Premium running shoes with advanced cushioning technology, perfect for long-distance running and daily workouts. Features breathable mesh upper and responsive foam midsole.",
                "price": 129.99,
                "category": "sports",
                "brand": "Nike",
                "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
                "tags": ["running", "athletic", "shoes", "sports", "workout"],
            },
            {
                "id": 2,
                "name": "Adidas Performance T-Shirt",
                "description": "High-performance sports t-shirt made from moisture-wicking fabric. Ideal for gym workouts, running, and athletic activities. Available in multiple colors.",
                "price": 34.99,
                "category": "clothing",
                "brand": "Adidas",
                "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400",
                "tags": ["t-shirt", "sports", "athletic", "workout", "gym"],
            },
            {
                "id": 3,
                "name": "Premium Yoga Mat",
                "description": "Non-slip yoga mat with excellent grip and cushioning. Perfect for yoga, pilates, and meditation. Made from eco-friendly materials.",
                "price": 49.99,
                "category": "sports",
                "brand": "Lululemon",
                "image_url": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400",
                "tags": ["yoga", "mat", "fitness", "meditation", "pilates"],
            },
            {
                "id": 4,
                "name": "Wireless Bluetooth Headphones",
                "description": "High-quality wireless headphones with noise cancellation. Perfect for workouts, commuting, and music listening. Long battery life and comfortable fit.",
                "price": 89.99,
                "category": "electronics",
                "brand": "Sony",
                "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
                "tags": ["headphones", "wireless", "bluetooth", "music", "audio"],
            },
            {
                "id": 5,
                "name": "Casual Denim Jacket",
                "description": "Classic denim jacket with modern styling. Versatile design suitable for casual and semi-formal occasions. Comfortable fit with multiple pockets.",
                "price": 79.99,
                "category": "clothing",
                "brand": "Levi's",
                "image_url": "https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=400",
                "tags": ["jacket", "denim", "casual", "fashion", "outerwear"],
            },
            {
                "id": 6,
                "name": "Smart Fitness Watch",
                "description": "Advanced fitness tracking watch with heart rate monitoring, GPS, and sleep tracking. Water-resistant and compatible with smartphones.",
                "price": 199.99,
                "category": "electronics",
                "brand": "Fitbit",
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400",
                "tags": ["watch", "fitness", "smartwatch", "tracking", "health"],
            },
            {
                "id": 7,
                "name": "Organic Cotton Hoodie",
                "description": "Comfortable hoodie made from 100% organic cotton. Perfect for casual wear and light outdoor activities. Sustainable and eco-friendly.",
                "price": 59.99,
                "category": "clothing",
                "brand": "Patagonia",
                "image_url": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=400",
                "tags": ["hoodie", "cotton", "casual", "organic", "sustainable"],
            },
            {
                "id": 8,
                "name": "Portable Bluetooth Speaker",
                "description": "Compact wireless speaker with impressive sound quality. Waterproof design perfect for outdoor activities, parties, and travel.",
                "price": 69.99,
                "category": "electronics",
                "brand": "JBL",
                "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
                "tags": ["speaker", "bluetooth", "portable", "wireless", "audio"],
            },
            {
                "id": 9,
                "name": "Professional Camera Lens",
                "description": "High-quality camera lens for professional photography. Excellent image quality with wide aperture for beautiful bokeh effects.",
                "price": 299.99,
                "category": "electronics",
                "brand": "Canon",
                "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=400",
                "tags": ["camera", "lens", "photography", "professional", "optical"],
            },
            {
                "id": 10,
                "name": "Eco-Friendly Water Bottle",
                "description": "Reusable water bottle made from sustainable materials. Keeps drinks cold for 24 hours and hot for 12 hours. Perfect for daily use.",
                "price": 24.99,
                "category": "home",
                "brand": "Hydro Flask",
                "image_url": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400",
                "tags": [
                    "water bottle",
                    "reusable",
                    "eco-friendly",
                    "sustainable",
                    "insulated",
                ],
            },
        ]

        self.products = sample_products
        self.save_products()
        logger.info("Created sample product catalog")

    def save_products(self) -> None:
        """Save products to the JSON file."""
        try:
            with open(self.catalog_file, "w", encoding="utf-8") as f:
                json.dump(self.products, f, indent=4, ensure_ascii=False)
            logger.info(f"Saved {len(self.products)} products to catalog")
        except Exception as e:
            logger.error(f"Error saving products: {str(e)}")

    def get_all_products(self) -> List[Dict[str, Any]]:
        """
        Get all products in the catalog.

        Returns:
            List[Dict[str, Any]]: List of all products
        """
        return self.products.copy()

    def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a product by its ID.

        Args:
            product_id (int): Product ID

        Returns:
            Optional[Dict[str, Any]]: Product if found, None otherwise
        """
        for product in self.products:
            if product["id"] == product_id:
                return product
        return None

    def search_products(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Search products using text similarity.

        Args:
            query (str): Search query
            limit (int): Maximum number of results

        Returns:
            List[Dict[str, Any]]: List of matching products
        """
        if not self.products:
            return []

        # Create product descriptions for comparison
        product_texts = []
        for product in self.products:
            text = f"{product['name']} {product['description']}"
            if "tags" in product:
                text += f" {' '.join(product['tags'])}"
            product_texts.append(text)

        try:
            # Vectorize all texts
            all_texts = [query] + product_texts
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)

            # Calculate similarities
            similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

            # Get top matches
            top_indices = similarities[0].argsort()[-limit:][::-1]

            matches = []
            for idx in top_indices:
                if similarities[0][idx] > 0.1:  # Minimum similarity threshold
                    matches.append(self.products[idx])

            return matches

        except Exception as e:
            logger.error(f"Error in product search: {str(e)}")
            # Fallback: simple keyword matching
            return self._keyword_search(query, limit)

    def _keyword_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """
        Simple keyword-based search as fallback.

        Args:
            query (str): Search query
            limit (int): Maximum number of results

        Returns:
            List[Dict[str, Any]]: List of matching products
        """
        query_lower = query.lower()
        matches = []

        for product in self.products:
            score = 0
            product_text = f"{product['name']} {product['description']}".lower()

            # Check for exact matches
            if query_lower in product_text:
                score += 10

            # Check for word matches
            query_words = query_lower.split()
            for word in query_words:
                if word in product_text:
                    score += 1

            if score > 0:
                matches.append((product, score))

        # Sort by score and return top results
        matches.sort(key=lambda x: x[1], reverse=True)
        return [product for product, score in matches[:limit]]

    def recommend_products(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend products based on user query.

        Args:
            query (str): User's query
            limit (int): Maximum number of recommendations

        Returns:
            List[Dict[str, Any]]: List of recommended products
        """
        # Use search functionality for recommendations
        recommendations = self.search_products(query, limit)

        # If no direct matches, try category-based recommendations
        if not recommendations:
            recommendations = self._category_based_recommendations(query, limit)

        return recommendations

    def _category_based_recommendations(
        self, query: str, limit: int
    ) -> List[Dict[str, Any]]:
        """
        Provide category-based recommendations when direct search fails.

        Args:
            query (str): User's query
            limit (int): Maximum number of recommendations

        Returns:
            List[Dict[str, Any]]: List of recommended products
        """
        query_lower = query.lower()

        # Define category keywords
        category_keywords = {
            "sports": [
                "sports",
                "athletic",
                "running",
                "gym",
                "workout",
                "fitness",
                "exercise",
            ],
            "clothing": [
                "shirt",
                "t-shirt",
                "pants",
                "jeans",
                "dress",
                "jacket",
                "shoes",
                "clothes",
            ],
            "electronics": [
                "phone",
                "laptop",
                "computer",
                "headphones",
                "camera",
                "tech",
                "electronic",
            ],
            "home": ["furniture", "home", "kitchen", "decor", "household"],
        }

        # Find matching category
        matching_category = None
        for category, keywords in category_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                matching_category = category
                break

        if matching_category:
            category_products = [
                product
                for product in self.products
                if product.get("category") == matching_category
            ]
            return category_products[:limit]

        # If no category match, return random products
        import random

        return random.sample(self.products, min(limit, len(self.products)))

    def add_product(self, product: Dict[str, Any]) -> bool:
        """
        Add a new product to the catalog.

        Args:
            product (Dict[str, Any]): Product information

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate new ID
            max_id = max([p["id"] for p in self.products]) if self.products else 0
            product["id"] = max_id + 1

            self.products.append(product)
            self.save_products()
            logger.info(f"Added product: {product['name']}")
            return True
        except Exception as e:
            logger.error(f"Error adding product: {str(e)}")
            return False

    def update_product(self, product_id: int, updates: Dict[str, Any]) -> bool:
        """
        Update an existing product.

        Args:
            product_id (int): Product ID
            updates (Dict[str, Any]): Product updates

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            for i, product in enumerate(self.products):
                if product["id"] == product_id:
                    self.products[i].update(updates)
                    self.save_products()
                    logger.info(f"Updated product: {product_id}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error updating product: {str(e)}")
            return False

    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product from the catalog.

        Args:
            product_id (int): Product ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.products = [p for p in self.products if p["id"] != product_id]
            self.save_products()
            logger.info(f"Deleted product: {product_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}")
            return False
