import React from 'react';

function Footer() {
    return (
        <footer className="bg-white border-t mt-auto">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div className="flex flex-col md:flex-row justify-between items-center">
                    <div className="text-center md:text-left mb-4 md:mb-0">
                        <p className="text-sm text-gray-600">
                            © 2025 Commerce AI Agent. Built by Purva Daga.
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                            Inspired by Amazon's Rufus
                        </p>
                    </div>
                    
                    <div className="flex items-center space-x-6 text-sm text-gray-500">
                        <span>Features</span>
                        <span>•</span>
                        <span>General Conversation</span>
                        <span>•</span>
                        <span>Product Recommendations</span>
                        <span>•</span>
                        <span>Image-Based Search</span>
                    </div>
                </div>
            </div>
        </footer>
    );
}

export default Footer;
