import React from 'react';
import { cardData } from './cardData';

export function Cards(){
    return (
        <div className='grid grid-cols-4 gap-4 bg-gray-800'>
            {cardData.map((card, index) => (
                    <div className="w-48 h-32" key={index}>
                        <img
                            src={`${card.image}`}
                            alt={`Card ${index + 1}`}
                            className="w-48 h-32" // Set the width and height according to your desired size
                        />
                    <p className="text-white">{card.description}</p>
                    </div>
                ))}
        </div>
    )
}
