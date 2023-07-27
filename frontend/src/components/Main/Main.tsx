import React, { useState, useEffect } from 'react';
import { cardData } from '../Cards/cardData';

export const Cards: React.FC = () => {
    const [images, setImages] = useState<string[]>([]);

    useEffect(() => {
        // Load the images dynamically
        Promise.all(
            cardData.map((card) => import(`../../${card.image}`))
        ).then((importedImages) => {
            // Store the image URLs in state once loaded
            setImages(importedImages.map((image) => image.default));
        });
    }, []);
    return (
        <div className='card-grid'>
            {images.map((image, index) => (
                <div className="card" key={index}>
                    <img src={image} alt={`Card ${index + 1}`} />
                    <p>{cardData[index].description}</p>
                </div>
            ))}
        </div>
    )
}
