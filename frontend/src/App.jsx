import React, { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import { Button, Input, Form, message } from 'antd';
import authService from './services/authService';
import TokenConfirmationPage from './TokenConfirmationPage'; // Импортируем компонент
import 'antd/dist/reset.css';  // Сброс стилей Ant Design
import './index.css';  // Tailwind CSS стили
import Home from './Home';

const App = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const user = authService.getCurrentUser();
    if (user) {
      setCurrentUser(user);
    }
  }, []);

  const handleRegister = async (values) => {
    try {
      const userData = {
        email: values.email,
        username: values.username,
        password: values.password,
        is_active: true,
        is_superuser: false,
        is_verified: false,
        role_id: 0
      };

      await authService.register(userData);
      message.success('Registration successful');

      // Отправляем запрос на сервер для запроса токена подтверждения
      await authService.requestVerifyToken(values.email);

      // Перенаправляем пользователя на страницу с вводом токена
      navigate('/token-confirmation');
    } catch (error) {
      message.error('Registration failed');
    }
  };

  const handleLogin = async (values) => {
    try {
      const user = await authService.login(values.email, values.password);
      setCurrentUser(user);
      message.success('Login successful');
      navigate('/games');
    } catch (error) {
      message.error('Login failed');
    }
  };

  const handleLogout = () => {
    authService.logout();
    setCurrentUser(null);
    message.success('Logout successful');
    navigate('/');
  };

  return (
    <Routes>
      <Route path="/" element={
        <div className="flex justify-center items-center h-screen bg-gray-100">
          <div className="p-6 bg-white rounded shadow-lg">
            {currentUser ? (
              <>
                <h1 className="text-2xl font-bold mb-4">Welcome, {currentUser.username}</h1>
                <Button type="primary" onClick={handleLogout} className="bg-red-500 hover:bg-red-700">
                  Logout
                </Button>
              </>
            ) : (
              <>
                <h1 className="text-2xl font-bold mb-4">Please Log In</h1>
                <Form
                  name="login"
                  initialValues={{ remember: true }}
                  onFinish={handleLogin}

                >
                  <Form.Item
                    name="email"
                    rules={[{ required: true, message: 'Please input your email!' }]}
                  >
                    <Input placeholder="Email" />
                  </Form.Item>

                  <Form.Item
                    name="password"
                    rules={[{ required: true, message: 'Please input your password!' }]}
                  >
                    <Input.Password placeholder="Password" />
                  </Form.Item>

                  <Form.Item>
                    <Button type="primary" htmlType="submit" className="bg-blue-500 hover:bg-blue-700">
                      Login
                    </Button>
                  </Form.Item>
                </Form>
                <Button type="primary" onClick={() => navigate('/register')} className="bg-green-500 hover:bg-green-700">
                  Register
                </Button>
              </>
            )}
          </div>
        </div>
      } />
      <Route path="/home" element={<Home />} />
      <Route path="/register" element={
        <div className="flex justify-center items-center h-screen bg-gray-100">
          <div className="p-6 bg-white rounded shadow-lg">
            <h1 className="text-2xl font-bold mb-4">Register</h1>
            <Form
              name="register"
              onFinish={handleRegister}
              ClassName="mx-auto max-w-md"
            >
              <Form.Item
                name="email"
                rules={[{ required: true, message: 'Please input your email!' }]}
              >
                <Input placeholder="Email" />
              </Form.Item>

              <Form.Item
                name="username"
                rules={[{ required: true, message: 'Please input your username!' }]}
              >
                <Input placeholder="Username" />
              </Form.Item>

              <Form.Item
                name="password"
                rules={[{ required: true, message: 'Please input your password!' }]}
              >
                <Input.Password placeholder="Password" />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" className="bg-blue-500 hover:bg-blue-700">
                  Register
                </Button>
              </Form.Item>
            </Form>
          </div>
        </div>
      } />
      <Route path="/token-confirmation" element={<TokenConfirmationPage />} />
    </Routes>
  );
};

export default App;
