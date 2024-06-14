import React, {useEffect, useState} from 'react';
import {Button, Card, Col, Form, Input, Layout, Menu, message, Modal, Row, theme,} from 'antd';
import axios from 'axios';
import {HomeOutlined, LogoutOutlined, RightCircleOutlined, TeamOutlined, UserOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";
import EditTeamModal from './EditTeamModal';
import UrlAddr from "../Url/UrlAddr.js";

const {Content, Footer, Sider} = Layout;


const MyTeams = () => {
    const [teams, setTeams] = useState([]);
    const [loading, setLoading] = useState(true);
    const [collapsed, setCollapsed] = useState(false);
    const [editTeam, setEditTeam] = useState(null);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [form] = Form.useForm();
    const [isEditModalVisible, setIsEditModalVisible] = useState(false);
    const navigate = useNavigate();

    const {
        token: {borderRadiusLG},
    } = theme.useToken();
    useEffect(() => {
        const fetchTeams = async () => {
            try {
                const response = await axios.get(UrlAddr + '/teams/my/', {
                    withCredentials: true
                });
                setTeams(response.data.data);
                setLoading(false);
            } catch (error) {
                message.error('Не удалось загрузить команды.');
                setLoading(false);
            }
        };

        fetchTeams();
    }, []);

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

    const showModal = () => {
        setIsModalVisible(true);
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const handleEditClick = (team) => {
        setEditTeam(team);
        setIsEditModalVisible(true);
    };


    const handleCreateTeam = async (values) => {
        try {
            await axios.post(UrlAddr + '/teams/', values, {
                withCredentials: true,
            });
            message.success('Команда успешно создана');
            setIsModalVisible(false);
        } catch (error) {
            message.error('Не удалось создать команду');
            console.error('Error:', error);
        }
    };

    const handleDelete = async (team) => {
        try {
            await axios.delete(UrlAddr + `/teams/${team.id}`, {
                withCredentials: true,
            });
        } catch (error) {
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
                        Мои команды
                    </h1>

                    <div style={{padding: '20px'}}>
                        <Row gutter={[16, 16]}>
                            {loading ? (
                                <p>Загрузка...</p>
                            ) : (
                                teams.map(team => (
                                    <Col key={team.id} xs={24} sm={12} md={8} lg={6}>
                                        <Card title={team.id}
                                              actions={[
                                                  // eslint-disable-next-line react/jsx-key
                                                  <Button onClick={() => handleEditClick(team)}>Изменить</Button>,
                                                  // eslint-disable-next-line react/jsx-key
                                                  <Button danger onClick={() => handleDelete(team)}>Удалить</Button>
                                              ]}>
                                            <p>1.
                                                Диагональный: {team && team.opposite === null ? "позиция свободна" : team && team.opposite}</p>
                                            <p>2. Доигровщик
                                                1: {team && team.outside_1 === null ? "позиция свободна" : team && team.outside_1}</p>
                                            <p>3. Доигровщик
                                                2: {team && team.outside_2 === null ? "позиция свободна" : team && team.outside_2}</p>
                                            <p>4.
                                                Связующий: {team && team.setter === null ? "позиция свободна" : team && team.setter}</p>
                                            <p>5. Центральный
                                                1: {team && team.middle_1 === null ? "позиция свободна" : team && team.middle_1}</p>
                                            <p>6. Центральный
                                                2: {team && team.middle_2 === null ? "позиция свободна" : team && team.middle_2}</p>
                                            <p>7.
                                                Либеро: {team && team.libero === null ? "позиция свободна" : team && team.libero}</p>
                                            <p>Удалить команду можно, если нет игр, где команда задействована</p>
                                        </Card>
                                    </Col>
                                ))
                            )}
                        </Row>
                        {editTeam && (
                            <EditTeamModal
                                visible={isEditModalVisible}
                                team={editTeam}
                                onClose={() => setIsEditModalVisible(false)}
                            />
                        )}
                        <Button type="primary" onClick={showModal}>Создать команду</Button>
                        <Modal
                            title="Создать команду"
                            open={isModalVisible}
                            onCancel={handleCancel}
                            footer={null}
                        >
                            <Form
                                form={form}
                                onFinish={handleCreateTeam}
                                initialValues={{
                                    creator: null,
                                    opposite: null,
                                    outside_1: null,
                                    outside_2: null,
                                    setter: null,
                                    middle_1: null,
                                    middle_2: null,
                                    libero: null,
                                }}
                            >
                                <Form.Item
                                    label="Диагональный"
                                    name="opposite"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item
                                    label="Доигровщик 1"
                                    name="outside_1"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item
                                    label="Доигровщик 2"
                                    name="outside_2"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>

                                <Form.Item
                                    label="Связующий"
                                    name="setter"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item
                                    label="Центральный 1"
                                    name="middle_1"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item
                                    label="Центральный 2"
                                    name="middle_2"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>
                                <Form.Item
                                    label="Либеро"
                                    name="libero"
                                    rules={[{message: 'Введите ID игрока'}]}
                                >
                                    <Input/>
                                </Form.Item>

                                <Form.Item>
                                    <Button type="primary" htmlType="submit">
                                        Создать
                                    </Button>
                                </Form.Item>
                            </Form>
                        </Modal>
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

export default MyTeams;
