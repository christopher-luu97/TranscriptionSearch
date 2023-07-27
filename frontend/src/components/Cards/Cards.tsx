import React from 'react';
import { cardData } from './cardData';

export const Cards: React.FC = () => {
    console.log('cardData:', cardData); // Log the cardData array

    return (
        <div className='card-grid'>
            {cardData.map((card, index) => (
                    <div className="card" key={index}>
                    <img src={`${process.env.PUBLIC_URL}/${card.image}`} alt={`Card ${index + 1}`} />
                    <p>{card.description}</p>
                    </div>
                ))}
        </div>
    )
}
