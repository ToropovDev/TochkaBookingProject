import {useState} from 'react';
import {HomeOutlined, LogoutOutlined, RightCircleOutlined, TeamOutlined, UserOutlined} from '@ant-design/icons';
import {Layout, Menu, message, theme} from 'antd';
import GamesList from "./GamesList.jsx";
import {Link, useNavigate} from "react-router-dom";
import axios from "axios";
import UrlAddr from "../Url/UrlAddr.js";


const {Content, Footer, Sider} = Layout;
const Games = () => {
    const [collapsed, setCollapsed] = useState(false);
    const navigate = useNavigate();

    const {
        token: {borderRadiusLG},
    } = theme.useToken();

    const handleLogout = async () => {
        try {
            await axios.post(UrlAddr + '/auth/logout', {}, {withCredentials: true});
            message.success('Вы успешно вышли из системы');
            navigate('/');
        } catch (error) {
            message.error('Не удалось выполнить выход из системы');
            console.error('Error:', error);
        }
    };

    return (
        <Layout
            style={{
                minHeight: '100vh',
            }}
        >
            <Sider collapsible collapsed={collapsed} onCollapse={(value) => setCollapsed(value)}
            >
                <div className="demo-logo-vertical"/>
                <Menu theme="dark" defaultSelectedKeys={['1']} mode="inline">
                    <Menu.Item key="games" icon={<HomeOutlined/>}>
                        <Link to="/games">Игры</Link>
                    </Menu.Item>
                    <Menu.Item key="profile" icon={<UserOutlined/>}>
                        <Link to="/profile">Мой профиль</Link>
                    </Menu.Item>
                    <Menu.Item key="my_teams" icon={<TeamOutlined/>}>
                        <Link to="/my-teams">Мои команды</Link>
                    </Menu.Item>
                    <Menu.Item key="my_games" icon={<RightCircleOutlined/>}>
                        <Link to="/my-games">Мои игры</Link>
                    </Menu.Item>
                    <Menu.Item key="logout" icon={<LogoutOutlined/>} onClick={handleLogout}>
                        Выход
                    </Menu.Item>
                </Menu>

            </Sider>

            <Layout>
                <Content
                    style={{
                        margin: '0 16px',
                        padding: 24,
                        minHeight: 360,
                        borderRadius: borderRadiusLG,
                        marginTop: 20
                    }}
                >
                    <h1 style={{
                        textAlign: 'center',
                        fontSize: 32,
                        marginBottom: 16,
                    }}>
                        Все игры
                    </h1>
                    <GamesList/>

                </Content>
                <Footer
                    style={{
                        textAlign: 'center',
                    }}
                >
                    Запись на игру ©{new Date().getFullYear()} Created by ToropovDev
                </Footer>
            </Layout>
        </Layout>
    );
};
export default Games;