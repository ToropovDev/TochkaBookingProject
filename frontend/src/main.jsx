import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import 'antd/dist/reset.css'; // Импорт стилей Ant Design
import './index.css'; // Импорт глобальных стилей
import { BrowserRouter } from "react-router-dom"
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
      <App />
  </React.StrictMode>,

);
