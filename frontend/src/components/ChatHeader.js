import React from 'react';

function ChatHeader({ apiStatus, agentMode, setAgentMode }) {
    return (
        <div className="bg-gradient-to-r from-indigo-600 to-violet-700 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-md">
                    <span className="text-indigo-600 font-bold text-lg">S</span>
                </div>
                <div>
                    <h2 className="text-white font-semibold text-lg">ShopBot</h2>
                    <p className="text-indigo-100 text-sm">
                        {apiStatus === 'connected' ? 'Online' : 'Offline'}
                    </p>
                </div>
            </div>
            <div className="flex items-center space-x-2">
                <label className="text-white font-semibold">Agent Mode</label>
                <input
                    type="checkbox"
                    checked={agentMode}
                    onChange={() => setAgentMode(!agentMode)}
                    className="form-checkbox h-5 w-5 text-indigo-600 accent-violet-600"
                />
            </div>
        </div>
    );
}

export default ChatHeader; 