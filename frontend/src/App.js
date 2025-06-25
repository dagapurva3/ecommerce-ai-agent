import React, { useState, useEffect } from 'react';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header';
import Footer from './components/Footer';
import './index.css';

function App() {
    const [isLoading, setIsLoading] = useState(true);
    const [apiStatus, setApiStatus] = useState('checking');

    useEffect(() => {
        // Check API health on component mount
        checkApiHealth();
    }, []);

    const checkApiHealth = async () => {
        try {
            const response = await fetch('http://localhost:5000/');
            if (response.ok) {
                setApiStatus('connected');
            } else {
                setApiStatus('error');
            }
        } catch (error) {
            console.error('API health check failed:', error);
            setApiStatus('error');
        } finally {
            setIsLoading(false);
        }
    };

    if (isLoading) {
        return (
            <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Initializing Commerce AI Agent...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
            <Header apiStatus={apiStatus} />

            <main className="flex-1 flex flex-col items-center justify-center p-4">
                <div className="w-full max-w-4xl">
                    <div className="text-center mb-8">
                        <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4">
                            ShopBot
                        </h1>
                        <p className="text-xl text-gray-600 mb-2">
                            Your AI-Powered Shopping Assistant
                        </p>
                        <p className="text-gray-500">
                            Get personalized recommendations, search products, and enjoy intelligent shopping assistance
                        </p>
                    </div>

                    {apiStatus === 'error' && (
                        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                            <strong>Connection Error:</strong> Unable to connect to the backend API.
                            Please ensure the backend server is running on http://localhost:5000
                        </div>
                    )}

                    <ChatInterface apiStatus={apiStatus} />
                </div>
            </main>

            <Footer />
        </div>
    );
}

export default App;