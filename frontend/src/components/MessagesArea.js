import React from 'react';
import MessageBubble from './MessageBubble';

function MessagesArea({ messages, isLoading, messagesEndRef, renderBotMessage }) {
  return (
    <div className="h-96 overflow-y-auto p-6 bg-slate-50">
      {messages.map((msg, index) => (
        <MessageBubble
          key={index}
          message={msg.type === 'bot' ? renderBotMessage(msg.message) : msg.message}
          type={msg.type}
          timestamp={msg.timestamp}
        />
      ))}
      {isLoading && (
        <div className="flex justify-start mb-4">
          <div className="bg-slate-200 text-slate-800 rounded-lg rounded-bl-none px-4 py-2">
            <div className="flex space-x-1">
              <div className="w-2 h-2 bg-slate-500 rounded-full animate-bounce"></div>
              <div className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              <div className="w-2 h-2 bg-slate-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
            </div>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default MessagesArea; 