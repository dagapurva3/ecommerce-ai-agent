import React from 'react';

function MessageBubble({ message, type, timestamp }) {
    const formatTime = (timestamp) => {
        return new Date(timestamp).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });
    };

    return (
        <div className={`flex ${type === 'user' ? 'justify-end' : 'justify-start'} mb-4`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                type === 'user' 
                    ? 'bg-blue-600 text-white rounded-br-none' 
                    : 'bg-gray-200 text-gray-800 rounded-bl-none'
            }`}>
                <p className="text-sm whitespace-pre-wrap">{message}</p>
                <p className={`text-xs mt-1 ${
                    type === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}>
                    {formatTime(timestamp)}
                </p>
            </div>
        </div>
    );
}

export default MessageBubble;
