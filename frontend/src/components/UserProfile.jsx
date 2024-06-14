import React, {useEffect, useState} from 'react';
import axios from 'axios';
import {Link, useNavigate, useParams} from 'react-router-dom';
import {Descriptions, Layout, Menu, message, Spin, theme} from 'antd';
import {HomeOutlined, LogoutOutlined, RightCircleOutlined, TeamOutlined, UserOutlined} from "@ant-design/icons";
import UrlAddr from "../Url/UrlAddr.js";

const {Content, Footer, Sider} = Layout;

const UserProfile = () => {
    const {userId} = useParams();
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);
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

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const response = await axios.get(UrlAddr + `/user/${userId}`, {
                    headers: {
                        "accept": "application/json",
                    },
                    withCredentials: true,
                });
                setUser(response.data.data);
            } catch (error) {
                message.error('Failed to fetch user information');
                console.error('Error:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchUser();
    }, [userId]);

    if (loading) {
        return <Spin size="large"/>;
    }

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
                        marginTop: 100
                    }}
                >

                    <div>
                        <Descriptions title="User Info" bordered>
                            <Descriptions.Item label="Юзернейм">{user.username}</Descriptions.Item>
                            <Descriptions.Item label="Email">{user.email}</Descriptions.Item>
                            <Descriptions.Item label="Сыграно игр">{user.games_played}</Descriptions.Item>
                            <Descriptions.Item label="Организовано игр">{user.games_organized}</Descriptions.Item>
                            <Descriptions.Item label="ID">{user.id}</Descriptions.Item>

                        </Descriptions>
                    </div>

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

export default UserProfile;
