import React from 'react';
import { Card } from 'antd';

const GameCard = ({ game }) => {
  return (
    <div className='m-2'>
      <Card
        title={game.name}
        extra={<a href="#">Больше</a>}
        style={{
          width: 300,
        }}
      >
        <p>{game.id}</p>
        <p>{game.place}</p>
        {/* Добавьте другие данные игры, если нужно */}
      </Card>
    </div>
  );
};

export default GameCard;
