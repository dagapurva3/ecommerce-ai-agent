import React from 'react';

function Header({ apiStatus }) {
    const getStatusColor = () => {
        switch (apiStatus) {
            case 'connected':
                return 'bg-green-500';
            case 'error':
                return 'bg-red-500';
            default:
                return 'bg-yellow-500';
        }
    };

    const getStatusText = () => {
        switch (apiStatus) {
            case 'connected':
                return 'Connected';
            case 'error':
                return 'Disconnected';
            default:
                return 'Checking...';
        }
    };

    return (
        <header className="bg-white shadow-sm border-b">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center py-4">
                    <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                            <span className="text-white font-bold text-sm">S</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-semibold text-gray-900">Commerce AI Agent</h1>
                            <p className="text-sm text-gray-500">Powered by AI</p>
                        </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                        <div className="flex items-center space-x-2">
                            <div className={`w-2 h-2 rounded-full ${getStatusColor()}`}></div>
                            <span className="text-sm text-gray-600">{getStatusText()}</span>
                        </div>
                        
                        <div className="hidden md:flex items-center space-x-4 text-sm text-gray-500">
                            <span>Features</span>
                            <span>•</span>
                            <span>Product Search</span>
                            <span>•</span>
                            <span>AI Recommendations</span>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}

export default Header;
