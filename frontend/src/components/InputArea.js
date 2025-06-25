import React from 'react';

function InputArea({
  query,
  setQuery,
  handleSubmit,
  handleImageUpload,
  handleKeyPress,
  isLoading,
  apiStatus,
  isDragActive,
  handleDragOver,
  handleDragLeave,
  handleDrop
}) {
  return (
    <div
      className={`border-t bg-white p-4 ${isDragActive ? 'border-4 border-emerald-400 bg-emerald-50' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      <form onSubmit={handleSubmit} className="flex space-x-2 items-center">
        <label className="bg-emerald-600 hover:bg-emerald-700 text-white px-3 py-1 rounded cursor-pointer flex items-center shadow" title="Upload an image to search for similar products">
          <input
            type="file"
            accept="image/*"
            onChange={(e) => {
              handleImageUpload(e);
              e.target.value = '';
            }}
            style={{ display: 'none' }}
            disabled={isLoading || apiStatus !== 'connected'}
          />
          <span role="img" aria-label="Upload">📷</span> <span className="ml-1 hidden sm:inline">Search with Image</span>
        </label>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything about products, recommendations, or just chat..."
          className="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
          disabled={isLoading || apiStatus !== 'connected'}
          title="Type your message or product request here"
        />
        <button
          type="submit"
          disabled={isLoading || apiStatus !== 'connected' || !query.trim()}
          className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors shadow"
          title="Send your message"
        >
          {isLoading ? (
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
          ) : (
            'Send'
          )}
        </button>
      </form>
      <div className="mt-3 flex flex-wrap gap-2">
        <span className="font-semibold text-xs text-slate-500 mr-2">📝 Text-Based:</span>
        {['Recommend running shoes', 'Show me t-shirts', 'Find electronics'].map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => setQuery(suggestion)}
            className="px-3 py-1 text-sm bg-indigo-100 text-indigo-700 rounded-full hover:bg-indigo-200 transition-colors shadow"
            title={`Quick suggestion: ${suggestion}`}
          >
            {suggestion}
          </button>
        ))}
        <div className="w-full h-0" />
        <span className="font-semibold text-xs text-slate-500 mr-2 mt-2">🖼️ Image-Based:</span>
        {['A blue sports t-shirt', 'Black running shoes', 'A picture of wireless headphones'].map((suggestion) => (
          <button
            key={suggestion}
            onClick={() => setQuery(suggestion)}
            className="px-3 py-1 text-sm bg-emerald-100 text-emerald-700 rounded-full hover:bg-emerald-200 transition-colors shadow"
            title={`Quick suggestion: ${suggestion}`}
          >
            {suggestion}
          </button>
        ))}
        <div className="w-full text-center text-xs text-emerald-700 mt-2">
          {isDragActive ? 'Drop your image here to search!' : 'Or drag and drop an image anywhere in this area.'}
        </div>
      </div>
    </div>
  );
}

export default InputArea; 