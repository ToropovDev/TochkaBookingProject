import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Form, Input, Button, message } from 'antd';
import authService from './services/authService';

const TokenConfirmationPage = () => {
  const [token, setToken] = useState('');
  const navigate = useNavigate();

const handleTokenConfirmation = async () => {
  try {
    await authService.verifyToken(token);
    message.success('Token verification successful');
    navigate('/home'); // Перенаправляем пользователя на главную страницу после успешного подтверждения токена
  } catch (error) {
    message.error('Token verification failed');
  }
};


  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="p-6 bg-white rounded shadow-lg">
        <h1 className="text-2xl font-bold mb-4">Enter Token</h1>
        <Form
          name="tokenConfirmation"
          ClassName="mx-auto max-w-md"
          onFinish={handleTokenConfirmation}
        >
          <Form.Item
            name="token"
            rules={[{ required: true, message: 'Please input the token!' }]}
          >
            <Input placeholder="Token" value={token} onChange={(e) => setToken(e.target.value)} />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit">
              Confirm
            </Button>
          </Form.Item>
        </Form>
      </div>
    </div>
  );
};

export default TokenConfirmationPage;
