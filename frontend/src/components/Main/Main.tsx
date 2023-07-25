import React from 'react';

// Define the data for the cards
const cardData = [
  {
    image: 'image1.jpg',
    description: 'Description 1',
  },
  {
    image: 'image2.jpg',
    description: 'Description 2',
  },
  // Add more card data as needed
];

const Main: React.FC = () => {
  return (
    <div className="App">
      <h1>Card Grid</h1>
      <div className="card-grid">
        {cardData.map((card, index) => (
          <div className="card" key={index}>
            <img src={card.image} alt={`Card ${index + 1}`} />
            <p>{card.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Main;
