import React, { useState } from 'react';
import axios from 'axios';
import { Form, Input, Button, Card, Alert } from 'antd';
import { useNavigate } from 'react-router-dom';

const Register = () => {
  const navigate = useNavigate(); // Получаем функцию для навигации
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const onFinish = (values) => {
    setLoading(true);
    setError(null);

    const data = {
      email: values.email,
      password: values.password,
      is_active: true,
      is_superuser: false,
      is_verified: false,
      username: values.username,
      role_id: 0
    };

    axios.post('http://127.0.0.1:8000/auth/register', data)
      .then(() => {
        // Запрос на /auth/request-verify-token после успешной регистрации
        return axios.post('http://127.0.0.1:8000/auth/request-verify-token', { email: values.email });
      })
      .then(() => {
        // Редирект на /auth/request-verify-token после успешного запроса на регистрацию и подтверждения
        navigate('/auth/request-verify-token', { state: { email: values.email } });
        navigate('/verify-token');
      })
      .catch(error => {
        setError(error.response?.data || 'Ошибка при отправке запроса на регистрацию');
      })
      .finally(() => {
        setLoading(false);
      });
  };

  return (
    <Card title="Регистрация" style={{ width: 400, margin: 'auto', marginTop: '50px' }}>
      {error && <Alert message="Ошибка" description={error} type="error" showIcon />}

      <Form
        form={form}
        layout="vertical"
        onFinish={onFinish}
      >
        <Form.Item
          label="Имя пользователя"
          name="username"
          rules={[{ required: true, message: 'Пожалуйста, введите имя пользователя!' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Электронная почта"
          name="email"
          rules={[{ required: true, message: 'Пожалуйста, введите электронную почту!', type: 'email' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="Пароль"
          name="password"
          rules={[{ required: true, message: 'Пожалуйста, введите пароль!' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Зарегистрироваться
          </Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default Register;
