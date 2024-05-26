import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; // замените на URL вашего backend

const login = async (email, password) => {
  const params = new URLSearchParams();
  params.append('grant_type', '');
  params.append('username', email);
  params.append('password', password);
  params.append('scope', '');
  params.append('client_id', '');
  params.append('client_secret', '');

  const response = await axios.post(`${API_URL}/auth/login`, params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  if (response.data.access_token) {
    localStorage.setItem('user', JSON.stringify(response.data));
  }
  return response.data;
};

const register = async (userData) => {
  const response = await axios.post(`${API_URL}/auth/register`, userData, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return response.data;
};

const requestVerifyToken = async (email) => {
  const userData = { email: email };

  const response = await axios.post(`${API_URL}/auth/request-verify-token`, userData, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return response.data;
};


const verifyToken = async (token) => {
  const tokenData = { token: token };

  const response = await axios.post(`${API_URL}/auth/verify`, tokenData, {
    headers: {
      'Content-Type': 'application/json',
    },
  });

  return response.data;
};

const logout = () => {
  localStorage.removeItem('user');
};

const getCurrentUser = () => {
  return JSON.parse(localStorage.getItem('user'));
};

export default {
  login,
  register,
  logout,
  getCurrentUser,
  requestVerifyToken,
  verifyToken,
};
