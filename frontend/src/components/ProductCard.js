import React from 'react';

function ProductCard({ product }) {
    const handleImageError = (e) => {
        // Fallback to a placeholder image if the original fails to load
        e.target.src = 'https://via.placeholder.com/300x200?text=Product+Image';
    };

    return (
        <div className="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
            <div className="aspect-w-16 aspect-h-9">
                <img 
                    src={product.image_url} 
                    alt={product.name} 
                    className="w-full h-48 object-cover"
                    onError={handleImageError}
                />
            </div>
            
            <div className="p-4">
                <div className="flex items-start justify-between mb-2">
                    <h3 className="text-lg font-semibold text-gray-800 line-clamp-2">
                        {product.name}
                    </h3>
                    <span className="text-lg font-bold text-blue-600 ml-2">
                        ${product.price.toFixed(2)}
                    </span>
                </div>
                
                <p className="text-gray-600 text-sm mb-3 line-clamp-3">
                    {product.description}
                </p>
                
                {product.brand && (
                    <p className="text-xs text-gray-500 mb-2">
                        Brand: {product.brand}
                    </p>
                )}
                
                {product.category && (
                    <span className="inline-block bg-blue-100 text-blue-800 text-xs px-2 py-1 rounded-full">
                        {product.category}
                    </span>
                )}
                
                <div className="mt-3 flex justify-between items-center">
                    <button className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-700 transition-colors">
                        View Details
                    </button>
                    <button className="text-blue-600 text-sm hover:text-blue-800 transition-colors">
                        Add to Cart
                    </button>
                </div>
            </div>
        </div>
    );
}

export default ProductCard;