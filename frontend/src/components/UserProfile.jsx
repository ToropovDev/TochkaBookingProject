import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Card, Spin, Alert } from 'antd';

const UserProfile = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/users/me')
      .then(response => {
        setUser(response.data.data);
        setLoading(false);
      })
      .catch(error => {
        setError(error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <Spin tip="Загрузка..."/>;
  }

  if (error) {
    return <Alert message="Ошибка" description="Не удалось загрузить данные пользователя." type="error" showIcon />;
  }

  return (
    <Card title="Мой Профиль" style={{ width: 300 }}>
      <p><strong>Username:</strong> {user.username}</p>
      <p><strong>Email:</strong> {user.email}</p>
    </Card>
  );
};

export default UserProfile;
