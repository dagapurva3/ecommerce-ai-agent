# Commerce AI Agent - Take-Home Assignment

## 🎯 Project Overview

A comprehensive AI-powered shopping assistant inspired by Amazon's Rufus, featuring intelligent product recommendations, natural language conversation, and simulated image-based search capabilities.

## ✨ Features

### 🤖 General Conversation
- Natural dialogue with the AI agent
- Questions like "What's your name?", "What can you do?", "How are you?"
- Contextual responses and helpful information

### 🔍 Text-Based Product Recommendations
- Intelligent product search and recommendations
- Queries like "Recommend me a t-shirt for sports"
- Semantic understanding of user preferences
- Category-based and keyword-based matching

### 🖼️ Image-Based Product Search (Simulated)
- Text description to product matching
- Descriptions like "A blue sports t-shirt"
- Advanced NLP processing for image descriptions
- Semantic similarity matching

### 🛍️ Product Catalog Management
- Comprehensive product database with 10+ sample products
- Categories: Sports, Clothing, Electronics, Home
- Detailed product information with images, prices, and descriptions
- Easy to extend and modify

### 🧠 Agent Mode: Gemini Integration
- When enabled, all chat and image queries are routed through Gemini, providing more insightful, context-rich, and creative responses.
- Gemini-powered product recommendations leverage advanced language and vision models for superior matching.
- Seamlessly toggle Agent Mode in the UI for a next-level AI experience.

## 🏗️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **Flask**: Lightweight web framework for API development
- **Flask-CORS**: Cross-origin resource sharing support
- **scikit-learn**: Machine learning for NLP and recommendations
- **NLTK**: Natural language processing toolkit
- **python-dotenv**: Environment variable management

### Frontend
- **React 18**: Modern component-based UI framework
- **Tailwind CSS**: Utility-first CSS framework for responsive design
- **Axios**: HTTP client for API communication
- **React Hooks**: State management and side effects

### Architecture Decisions

**Why Flask?**
- Lightweight and perfect for rapid API development
- Easy to understand and maintain
- Excellent for prototyping and production deployment
- Rich ecosystem of extensions

**Why React + Tailwind?**
- Component-based architecture for reusability
- Modern development experience with hooks
- Responsive design out of the box
- Excellent developer tools and debugging

**Why scikit-learn + NLTK?**
- Industry-standard libraries for NLP
- TF-IDF vectorization for semantic search
- Cosine similarity for product matching
- Comprehensive text preprocessing capabilities

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the backend server:**
   ```bash
   python app.py
   ```

   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The frontend will run on `http://localhost:3000`

## 📚 API Documentation

### Base URL
http://localhost:5000

### Endpoints

#### 1. Health Check
```http
GET /
```
**Response:**
```json
{
  "status": "healthy",
  "message": "Commerce AI Agent API is running",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "version": "1.0.0"
}
```

#### 2. General Chat
```http
POST /api/chat
Content-Type: application/json

{
  "query": "What's your name?"
}
```
**Response:**
```json
{
  "response": "I'm ShopBot, your AI-powered shopping assistant!",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### 3. Product Recommendations
```http
POST /api/recommend
Content-Type: application/json

{
  "query": "Recommend me a t-shirt for sports"
}
```
**Response:**
```json
{
  "products": [
    {
      "id": 2,
      "name": "Adidas Performance T-Shirt",
      "description": "High-performance sports t-shirt...",
      "price": 34.99,
      "category": "clothing",
      "brand": "Adidas",
      "image_url": "https://images.unsplash.com/...",
      "tags": ["t-shirt", "sports", "athletic"]
    }
  ],
  "query": "Recommend me a t-shirt for sports",
  "count": 1,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### 4. Image-Based Search
```http
POST /api/image_search
Content-Type: application/json

{
  "description": "A blue sports t-shirt"
}
```
**Response:**
```json
{
  "products": [
    {
      "id": 2,
      "name": "Adidas Performance T-Shirt",
      "description": "High-performance sports t-shirt...",
      "price": 34.99,
      "category": "clothing",
      "brand": "Adidas",
      "image_url": "https://images.unsplash.com/...",
      "tags": ["t-shirt", "sports", "athletic"]
    }
  ],
  "description": "A blue sports t-shirt",
  "count": 1,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

#### 5. Get All Products
```http
GET /api/products
```
**Response:**
```json
{
  "products": [...],
  "count": 10,
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```
#### 6. Agent Mode – Gemini-Powered Chat

```http
POST /api/agent_chat
Content-Type: application/json

{
  "query": "What are the best running shoes for summer?"
}
```
**Response:**
```json
{
  "response": "Gemini-powered answer...",
  "products": [ ... ],
  "timestamp": "..."
}
```

#### 7. Agent Mode – Gemini-Powered Image Search

```http
POST /api/agent_image
Content-Type: multipart/form-data

image: (binary image file)
prompt: "What products do you see?"
```
**Response:**
```json
{
  "response": "Gemini-powered vision analysis..."
}
```

## 🎮 Usage Examples

### General Conversation
- "What's your name?"
- "What can you do?"
- "How are you today?"
- "Tell me about yourself"

### Product Recommendations
- "Recommend running shoes"
- "Show me t-shirts for sports"
- "Find wireless headphones"
- "I need a yoga mat"

### Image-Based Search
- "A blue sports t-shirt"
- "Black running shoes"
- "Wireless headphones"
- "A comfortable hoodie"

## ��️ Project Structure

```
ecommerce-ai-agent/
├── backend/                        # Python Flask API and AI logic
│   ├── app.py                      # Main Flask application (API entry point)
│   ├── nlp_utils.py                # NLP processing utilities (intent, semantic search)
│   ├── product_catalog.py          # Product catalog management and recommendation logic
│   ├── products.json               # Sample product database (10+ products)
│   ├── requirements.txt            # Python dependencies
│   ├── .env                        # Environment variables (not committed)
│   └── .env.example                # Example environment config for setup
├── frontend/                       # React + Tailwind CSS frontend
│   ├── package.json                # Node.js dependencies and scripts
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   ├── public/
│   │   └── index.html              # HTML template
│   └── src/
│       ├── App.js                  # Main React component
│       ├── index.js                # React entry point
│       ├── index.css               # Global styles (Tailwind + custom)
│       └── components/             # Modular UI components
│           ├── ChatHeader.js       # Chat header with Agent Mode toggle
│           ├── ChatInterface.js    # Main chat interface logic
│           ├── Footer.js           # App footer
│           ├── Header.js           # App header
│           ├── InputArea.js        # User input and image upload
│           ├── MessageBubble.js    # Chat message bubble
│           ├── MessagesArea.js     # Chat history display
│           ├── ProductCard.js      # Product display card
│           └── ProductsDisplay.js  # Product results grid
└── README.md                       # Project documentation (this file)
```


## 🔧 Technical Implementation

### NLP Processing
- **Text Preprocessing**: Tokenization, lemmatization, stop word removal
- **Intent Recognition**: Pattern matching for conversation types
- **Feature Extraction**: Product attributes, categories, keywords
- **Semantic Search**: TF-IDF vectorization with cosine similarity

### Product Matching
- **Keyword Matching**: Direct text search with scoring
- **Category Matching**: Product categorization and filtering
- **Semantic Matching**: Advanced NLP-based similarity
- **Fallback Mechanisms**: Multiple search strategies

### Frontend Features
- **Real-time Chat**: Instant message display and typing indicators
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Error Handling**: Graceful API error management
- **Loading States**: User feedback during API calls

## 🚀 Deployment

### Local Development
Both frontend and backend run on localhost with hot reloading for development.

### Production Deployment
1. **Backend**: Deploy to platforms like Heroku, AWS, or DigitalOcean
2. **Frontend**: Build with `npm run build` and serve static files
3. **Environment Variables**: Configure API endpoints and secrets
4. **Database**: Replace JSON file with proper database (PostgreSQL, MongoDB)

## 🔮 Future Enhancements

### Immediate Improvements
- [ ] User authentication and profiles
- [ ] Shopping cart functionality
- [ ] Order processing and checkout
- [ ] Product reviews and ratings

### Advanced Features
- [ ] Real image processing with computer vision
- [ ] Machine learning for personalized recommendations
- [ ] Voice interface integration
- [ ] Multi-language support
- [ ] Advanced analytics and insights

## 🧑‍💻 Why Hire Me?

- **Full-stack expertise**: From backend APIs to frontend UX, I deliver robust, scalable, and maintainable solutions.
- **AI integration**: Demonstrated ability to leverage state-of-the-art models (Gemini) for real-world applications.
- **Clean code & documentation**: Codebase is readable, modular, and well-documented for teams.
- **Product thinking**: Features are designed with user experience and business value in mind.
- **Ownership**: This project is built end-to-end, with attention to detail and a passion for excellence.


## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is created for educational and demonstration purposes.

## 👨‍💻 Author

Created by Purva Daga for showcasing modern web development skills with AI integration.

---

**Note**: This is a demonstration project. The image-based search is simulated using text descriptions, as implementing actual computer vision would require additional infrastructure and time constraints.