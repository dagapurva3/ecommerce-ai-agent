import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ProductCard from './ProductCard';
import MessageBubble from './MessageBubble';
import ChatHeader from './ChatHeader';
import MessagesArea from './MessagesArea';
import ProductsDisplay from './ProductsDisplay';
import InputArea from './InputArea';

// Helper to clean up Gemini's Markdown-style response
function formatGeminiResponse(text) {
    if (!text) return '';
    // Replace leading "* " with a bullet
    let formatted = text.replace(/^\* /gm, '• ');
    // Remove remaining single asterisks used for emphasis
    formatted = formatted.replace(/\*/g, '');
    // Optionally, replace double newlines with <br/><br/> for spacing
    formatted = formatted.replace(/\n\n/g, '<br/><br/>');
    // Replace single newlines with <br/>
    formatted = formatted.replace(/\n/g, '<br/>');
    return formatted;
}

const REACT_APP_BACKEND_URL = process.env.REACT_APP_BACKEND_URL

function ChatInterface({ apiStatus }) {
    const [query, setQuery] = useState('');
    const [messages, setMessages] = useState([]);
    const [products, setProducts] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [lastFeature, setLastFeature] = useState(null);
    const [showProducts, setShowProducts] = useState(true);
    const messagesEndRef = useRef(null);
    const [agentMode, setAgentMode] = useState(false);
    const [isDragActive, setIsDragActive] = useState(false);

    // Welcome message on component mount
    useEffect(() => {
        const welcomeMessage = {
            type: 'bot',
            message: "👋 Hello! I'm ShopBot, your AI shopping assistant. I can help you with:\n\n" +
                "• 📝 Text-Based Product Recommendation (e.g., 'Recommend me a t-shirt for sports.')\n" +
                "• 🖼️ Image-Based Product Search (e.g., 'A blue sports t-shirt' or upload an image)\n" +
                "• 💬 General conversation\n\nWhat would you like to try?",
            timestamp: new Date().toISOString()
        };
        setMessages([welcomeMessage]);
    }, []);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, products]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!query.trim() || isLoading || apiStatus !== 'connected') return;

        const userMessage = {
            type: 'user',
            message: query,
            timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, userMessage]);
        setQuery('');
        setIsLoading(true);

        try {
            let response;
            const queryLower = query.toLowerCase();
            if (agentMode) {
                response = await axios.post(`${REACT_APP_BACKEND_URL}/api/agent_chat`, { query });

                // Show product recommendations if present
                setProducts(response.data.products || []);
                setLastFeature('agent');
                setShowProducts(!!(response.data.products && response.data.products.length > 0));

                const botMessage = {
                    type: 'bot',
                    message:
                        `<b>🤖 Agent Mode:</b> ${formatGeminiResponse(response.data.response)}` +
                        (response.data.products && response.data.products.length > 0
                            ? `<br/><br/>🛒 <b>Product Recommendations:</b> I found <b>${response.data.products.length}</b> product(s) for you.`
                            : "<br/><br/>🛒 <b>Product Recommendations:</b> Sorry, I couldn't find any products matching your request."),
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, botMessage]);
                return;
            }

            // Image-Based Product Search
            if (
                queryLower.includes('image') ||
                queryLower.includes('picture') ||
                queryLower.includes('photo') ||
                queryLower.includes('looks like') ||
                queryLower.startsWith('a ') // e.g., "A blue sports t-shirt"
            ) {
                response = await axios.post(`${REACT_APP_BACKEND_URL}/api/image_search`, { description: query });
                setProducts(response.data.products || []);
                setLastFeature('image');
                setShowProducts(true);
                const botMessage = {
                    type: 'bot',
                    message: response.data.products && response.data.products.length > 0
                        ? `🖼️ <b>Image-Based Product Search:</b> I found <b>${response.data.products.length}</b> product(s) matching your description.`
                        : "🖼️ <b>Image-Based Product Search:</b> Sorry, I couldn't find any products matching your description.",
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, botMessage]);
            }
            // Text-Based Product Recommendation
            else if (
                queryLower.includes('recommend') ||
                queryLower.includes('search') ||
                queryLower.includes('find') ||
                queryLower.includes('show me') ||
                queryLower.includes('looking for')
            ) {
                response = await axios.post(`${REACT_APP_BACKEND_URL}/api/recommend`, { query });
                setProducts(response.data.products || []);
                setLastFeature('text');
                setShowProducts(true);
                const botMessage = {
                    type: 'bot',
                    message: response.data.products && response.data.products.length > 0
                        ? `📝 <b>Text-Based Product Recommendation:</b> I found <b>${response.data.products.length}</b> product(s) that match your request.`
                        : "📝 <b>Text-Based Product Recommendation:</b> Sorry, I couldn't find any products matching your request.",
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, botMessage]);
            }
            // General conversation
            else {
                response = await axios.post(`${REACT_APP_BACKEND_URL}/api/chat`, { query });
                setProducts(response.data.products || []);
                setLastFeature('chat');
                setShowProducts(!!(response.data.products && response.data.products.length > 0));
                const botMessage = {
                    type: 'bot',
                    message: response.data.response,
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, botMessage]);
            }

        } catch (error) {
            console.error('API Error:', error);
            const errorMessage = {
                type: 'bot',
                message: "I'm sorry, I'm having trouble connecting to my services right now. Please try again in a moment.",
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    // NEW: Handle image upload
    const handleImageUpload = async (e) => {
        const file = e.target.files[0];
        if (!file || isLoading || apiStatus !== 'connected') return;

        setIsLoading(true);

        // Show user message
        setMessages(prev => [
            ...prev,
            {
                type: 'user',
                message: `Uploaded an image: ${file.name}`,
                timestamp: new Date().toISOString()
            }
        ]);

        try {
            if (agentMode) {
                // 1. Get Gemini agent response
                const formData = new FormData();
                formData.append('image', file);
                formData.append('prompt', "What products do you see?");
                const agentResponse = await axios.post(`${REACT_APP_BACKEND_URL}/api/agent_image`, formData, {
                    headers: { 'Content-Type': 'multipart/form-data' }
                });
                // console.log(agentResponse)

                // 2. Get product recommendations from chat API using Gemini's response
                const chatResponse = await axios.post(`${REACT_APP_BACKEND_URL}/api/chat`, {
                    query: agentResponse.data.response
                });
                // console.log(chatResponse)

                setProducts(chatResponse.data.products || []);
                setLastFeature('image');
                setShowProducts(true);

                // 3. Show Gemini response and recommendations as a bot message
                const botMessage = {
                    type: 'bot',
                    message: `<b>🤖 Agent Mode (Image):</b> ${formatGeminiResponse(agentResponse.data.response)}` +
                        (chatResponse.data.products && chatResponse.data.products.length > 0
                            ? `<br/><br/>🖼️ <b>Product Recommendations:</b> I found <b>${chatResponse.data.products.length}</b> product(s) matching your uploaded image.`
                            : "<br/><br/>🖼️ <b>Product Recommendations:</b> Sorry, I couldn't find any products matching your uploaded image."),
                    timestamp: new Date().toISOString()
                };
                setMessages(prev => [...prev, botMessage]);
                return;
            }

            const formData = new FormData();
            formData.append('image', file);

            const response = await axios.post(`${REACT_APP_BACKEND_URL}/api/image_upload`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });

            setProducts(response.data.products || []);
            setLastFeature('image');
            setShowProducts(true);

            const botMessage = {
                type: 'bot',
                message: response.data.products && response.data.products.length > 0
                    ? `🖼️ <b>Image-Based Product Search:</b> I found <b>${response.data.products.length}</b> product(s) matching your uploaded image.`
                    : "🖼️ <b>Image-Based Product Search:</b> Sorry, I couldn't find any products matching your uploaded image.",
                timestamp: new Date().toISOString()
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error('API Error:', error);
            setMessages(prev => [
                ...prev,
                {
                    type: 'bot',
                    message: "Sorry, there was a problem processing your image.",
                    timestamp: new Date().toISOString()
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    // Helper to render HTML in bot messages (for <b> tags)
    const renderBotMessage = (msg) => {
        return <span dangerouslySetInnerHTML={{ __html: msg }} />;
    };

    // Drag and drop handlers for image upload
    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(true);
    };
    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
    };
    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            const file = e.dataTransfer.files[0];
            // Create a synthetic event to reuse handleImageUpload
            const syntheticEvent = { target: { files: [file] } };
            handleImageUpload(syntheticEvent);
        }
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center dynamic-bg">
            <div className="w-full max-w-4xl mx-auto">
                <div className="bg-white rounded-2xl shadow-2xl overflow-hidden border border-slate-200">
                    <ChatHeader
                        apiStatus={apiStatus}
                        agentMode={agentMode}
                        setAgentMode={setAgentMode}
                    />
                    <MessagesArea
                        messages={messages}
                        isLoading={isLoading}
                        messagesEndRef={messagesEndRef}
                        renderBotMessage={renderBotMessage}
                    />
                    <ProductsDisplay
                        products={products}
                        showProducts={showProducts}
                        lastFeature={lastFeature}
                        setShowProducts={setShowProducts}
                    />
                    <InputArea
                        query={query}
                        setQuery={setQuery}
                        handleSubmit={handleSubmit}
                        handleImageUpload={handleImageUpload}
                        handleKeyPress={handleKeyPress}
                        isLoading={isLoading}
                        apiStatus={apiStatus}
                        isDragActive={isDragActive}
                        handleDragOver={handleDragOver}
                        handleDragLeave={handleDragLeave}
                        handleDrop={handleDrop}
                    />
                </div>
            </div>
        </div>
    );
}

export default ChatInterface;