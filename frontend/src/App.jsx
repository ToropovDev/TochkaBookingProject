import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { UserOutlined, UnorderedListOutlined, UserAddOutlined } from '@ant-design/icons';
import { Menu } from 'antd';
import axios from 'axios';
import GameCard from './components/GameCard.jsx';
import UserProfile from './components/UserProfile.jsx'; // Убедитесь, что путь правильный
import Register from './pages/Register';
import VerifyToken from "./pages/VerifyToken.jsx";

const items = [
  {
    key: 'sub1',
    label: 'Главное меню',
    type: 'group',
    children: [
        {
        key: 'register',
        label: <Link to="/register">Регистрация</Link>,
        type: 'item',
        icon: <UserAddOutlined />,
      },
      {
        key: 'profile',
        label: <Link to="/users/me">Мой Профиль</Link>,
        type: 'item',
        icon: <UserOutlined />,
      },
      {
        key: 'games',
        label: <Link to="/">Все игры</Link>, // Ведет на главную страницу
        type: 'item',
        icon: <UnorderedListOutlined />,
      },
    ],
  },
];

const App = () => {
  const [games, setGames] = useState([]);

  const fetchGames = () => {
    axios.get('http://127.0.0.1:8000/games/')
      .then((response) => {
        const gamesResponse = response.data.data;
        if (Array.isArray(gamesResponse)) {
          setGames(gamesResponse);
        } else {
          console.error('Received data is not an array');
        }
      })
      .catch((error) => {
        console.error('Error fetching games:', error);
      });
  };

  useEffect(() => {
    fetchGames();
  }, []);

  const onClick = (e) => { // Объявляем функцию onClick
    console.log('click ', e);
  };


  return (
    <div className='flex'>
      <Menu
          onClick={onClick}
          style={{width: 256}}
          defaultSelectedKeys={['1']}
          defaultOpenKeys={['sub1']}
          mode="inline"
          items={items}
          className='h-screen overflow-y-scroll'
      />
      <div className='flex flex-wrap'>
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/users/me" element={<UserProfile/>}/>
            <Route path="/verify-token" element={<VerifyToken/>}/>
        </Routes>
      </div>
      <div className='flex flex-wrap'>
        {games.map((game) => (
            <GameCard key={game.id} game={game}/>
        ))}
      </div>
    </div>
  );
};



export default App;
