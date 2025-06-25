import React from 'react';
import ProductCard from './ProductCard';

function ProductsDisplay({ products, showProducts, lastFeature, setShowProducts }) {
  if (!products.length || !showProducts) return null;
  return (
    <div className="border-t bg-white p-6 relative">
      <button
        className="absolute top-2 right-2 text-slate-400 hover:text-red-500 text-xl font-bold"
        onClick={() => setShowProducts(false)}
        aria-label="Close"
      >
        ×
      </button>
      <h3 className="text-lg font-semibold text-emerald-700 mb-4">
        {lastFeature === 'image' && <>🖼️ Image-Based Product Search Results</>}
        {lastFeature === 'text' && <>📝 Text-Based Product Recommendation Results</>}
        {lastFeature === 'chat' && <>Recommended Products</>}
      </h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map((product) => (
          <ProductCard key={product.id} product={product} />
        ))}
      </div>
    </div>
  );
}

export default ProductsDisplay; 