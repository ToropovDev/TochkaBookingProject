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
        <p>Место: {game.place}</p>
          <p>Время: {game.datetime}</p>
          <p></p>
      </Card>
    </div>
  );
};

export default GameCard;
