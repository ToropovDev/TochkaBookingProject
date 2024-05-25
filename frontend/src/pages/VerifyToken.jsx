import React, { useState } from 'react';
import { Card, Form, Input, Button, message } from 'antd';
import axios from 'axios';

const VerifyTokenPage = () => {
  const [token, setToken] = useState('');

  const onFinish = async (values) => {
    try {
      // Отправляем запрос на сервер
      const response = await axios.post('http://127.0.0.1:8000/auth/verify', { token });
      // Обрабатываем успешный ответ
      message.success(response.data.message);
    } catch (error) {
      // Обрабатываем ошибку
      message.error('Ошибка при отправке токена');
    }
  };

  return (
    <Card title="Подтверждение токена" style={{ width: 400, margin: 'auto', marginTop: '50px' }}>
      <Form
        layout="vertical"
        onFinish={onFinish}
      >
        <Form.Item
          label="Токен"
          name="token"
          rules={[{ required: true, message: 'Пожалуйста, введите токен' }]}
        >
          <Input value={token} onChange={e => setToken(e.target.value)} />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Подтвердить
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default VerifyTokenPage;
