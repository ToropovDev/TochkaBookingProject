import React, {useEffect, useState} from 'react';
import {Button, Card, DatePicker, Form, Input, Layout, Menu, message, Modal, Select, theme} from 'antd';
import axios from 'axios';
import {HomeOutlined, LogoutOutlined, RightCircleOutlined, TeamOutlined, UserOutlined} from "@ant-design/icons";
import {Link, useNavigate} from "react-router-dom";
import GameDetailsModal from "./GameDetailsModal.jsx";
import UrlAddr from "../Url/UrlAddr.js";

const {Content, Footer, Sider} = Layout;
const {Option} = Select;

function formatDate(isoString) {
    const date = new Date(isoString);
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);

    return `${day}.${month}.${year}`;
}

function formatTime(isoString) {
    const date = new Date(isoString);
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');

    return `${hours}:${minutes}`;
}

const MyGames = () => {
    const [games, setGames] = useState([]);
    const [collapsed, setCollapsed] = useState(false);
    const [modalVisible, setModalVisible] = useState(false);
    const [selectedGame, setSelectedGame] = useState(null);
    const [team1, setTeam1] = useState(null);
    const [team2, setTeam2] = useState(null);
    const [user1, setUser1] = useState(null);
    const [user2, setUser2] = useState(null);
    const [addGameModalVisible, setAddGameModalVisible] = useState(false);
    const [teams, setTeams] = useState([]);
    const [isModalVisible, setIsModalVisible] = useState(false);
    const [form] = Form.useForm();
    const [game_to_edit, setGame] = useState([]);
    const navigate = useNavigate();
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

    const {
        token: {borderRadiusLG},
    } = theme.useToken();

    const fetchMyGames = async () => {
        try {
            const response = await axios.get(UrlAddr + '/games/my/', {
                withCredentials: true,
            });
            setGames(response.data.data);
        } catch (error) {
            message.error('Не удалось загрузить игры');
            console.error('Error:', error);
        }
    };

    useEffect(() => {


        const fetchTeams = async () => {
            try {
                const response = await axios.get(UrlAddr + '/teams/');
                setTeams(response.data.data);
            } catch (error) {
                message.error('Failed to fetch teams');
                console.error('Error:', error);
            }
        };

        fetchMyGames();
        fetchTeams();
    }, []);

    const fetchTeam = async (teamId) => {
        try {
            const response = await axios.get(UrlAddr + `/teams/${teamId}`, {
                headers: {
                    "accept": "application/json",
                },
                withCredentials: true,
            });
            return response.data.data;
        } catch (error) {
            console.error('Error fetching team:', error);
            return null;
        }
    };

    const fetchUser = async (userId) => {
        try {
            const response = await axios.get(UrlAddr + `/user/${userId}`, {
                headers: {
                    "accept": "application/json",
                },
                withCredentials: true,
            });
            return response.data.data;
        } catch (error) {
            console.error('Error fetching user:', error);
            return null;
        }
    };

    const openModal = async (gameId) => {
        try {
            const response = await axios.get(UrlAddr + `/games/${gameId}`, {
                headers: {
                    "accept": "application/json",
                },
                withCredentials: true,
            });
            const game = response.data.data;
            setSelectedGame(game);
            const team1Data = await fetchTeam(game.team_1);
            const team2Data = await fetchTeam(game.team_2);
            setTeam1(team1Data);
            setTeam2(team2Data);
            const user1Data = await fetchUser(team1Data.creator);
            const user2Data = await fetchUser(team2Data.creator);
            setUser1(user1Data);
            setUser2(user2Data);
            setModalVisible(true);
        } catch (error) {
            message.error('Failed to fetch game details');
            console.error('Error:', error);
        }
    };

    const closeModal = () => {
        setModalVisible(false);
        setSelectedGame(null);
    };

    const handleAddGame = () => {
        setAddGameModalVisible(true);
    };

    const showModalEdit = (game) => {
        setSelectedGame(game);
        setIsModalVisible(true);
        form.setFieldsValue({
            name: game.name,
            place: game.place,
        });
        setGame(game.id)
    };

    const handleCancel = () => {
        setIsModalVisible(false);
    };

    const showModal = (data) => {
        Modal.success({
            title: 'Результат запроса',
            content: (
                <div>
                    <p>Игра успешно добавлена!</p>
                    <Button type="primary" href={data.confirmation_url} target="_blank" rel="noopener noreferrer">
                        Оплатить
                    </Button>
                </div>
            ),
            onOk() {
                console.log('Ок');
            },
        });
    };


    const handleUpdateGame = async (values) => {
        const datetimeISO = new Date(values.datetime).toISOString().slice(0, -1); // Преобразуем дату в объект Date
        const params = new URLSearchParams({
            name: values.name,
            place: values.place,
            datetime: datetimeISO ? datetimeISO : null,
            status: values.status ? values.status : 0,
            level: values.level ? values.level : 0,
            team_1: values.team_1 ? values.team_1 : 0,
            team_2: values.team_2 ? values.team_2 : 0,
            amount: values.amount ? values.amount : 0,
        });
        try {
            await axios.patch(UrlAddr + `/games/${game_to_edit}/?${params.toString()}`, {}, {
                headers: {
                    "accept": "application/json",
                },
                withCredentials: true,
            });
            message.success('Данные игры успешно обновлены!');
            // Дополнительные действия, если необходимо
        } catch (error) {
            message.error('Не удалось обновить данные игры.');
            console.error('Error:', error);
        }
    };

    const handleAddGameSubmit = async (values) => {
        const datetimeISO = new Date(values.datetime).toISOString().slice(0, -1); // Преобразуем дату в объект Date
        const params = new URLSearchParams({
            name: values.name,
            place: values.place,
            datetime: datetimeISO,
            status: values.status,
            level: values.level,
            team_1: values.team_1,
            team_2: values.team_2,
            amount: values.amount,
        });

        try {
            const add_response = await axios.post(UrlAddr + `/games/?${params.toString()}`, {}, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded", // Установим правильный заголовок Content-Type
                },
                withCredentials: true,
            });
            message.success('Игра успешно добавлена');
            setAddGameModalVisible(false);
            // Обновим список игр
            const response = await axios.get(UrlAddr + '/games/');
            setGames(response.data.data);

            if (values.amount !== 0) {
                showModal(add_response.data.data);
            }
        } catch (error) {
            message.error('Не удалось добавить игру');
            console.error('Error:', error);
        }
    };

    const handleDelete = async (gameId) => {
        try {
            await axios.delete(UrlAddr + `/games/${gameId}`, {
                withCredentials: true,
            });
            message.success('Игра успешно удалена');
            fetchMyGames(); // Обновляем список игр после удаления
        } catch (error) {
            message.error('Не удалось удалить игру');
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
                        Мои игры
                    </h1>


                    <div style={{display: 'flex', flexWrap: 'wrap', gap: '20px'}}>
                        {games.map(game => (
                            <Card
                                key={game.id}
                                title={game.name}
                                style={{width: 300}}
                                actions={[
                                    // eslint-disable-next-line react/jsx-key
                                    <Button type="primary" onClick={() => showModalEdit(game)}>Изменить</Button>,
                                    // eslint-disable-next-line react/jsx-key
                                    <Button type="primary" danger onClick={() => handleDelete(game.id)}>Удалить</Button>
                                ]}
                            >
                                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                                    <div>
                                        <p><b>Место:</b> {game.place}</p>
                                        <p><b>Дата:</b> {formatDate(game.datetime)} {formatTime(game.datetime)}</p>
                                    </div>
                                    <div style={{alignSelf: 'flex-end'}}>
                                        <Button type="primary" onClick={() => openModal(game.id)}>
                                            Подробнее
                                        </Button>
                                    </div>
                                </div>
                            </Card>
                        ))}
                        <GameDetailsModal
                            visible={modalVisible}
                            game={selectedGame}
                            team1={team1}
                            team2={team2}
                            user1={user1}
                            user2={user2}
                            onClose={closeModal}
                        />
                    </div>
                    <Modal
                        title="Изменить игру"
                        open={isModalVisible}
                        onCancel={handleCancel}
                        footer={null}
                    >
                        <Form
                            form={form}
                            onFinish={handleUpdateGame}
                        >
                            <Form.Item
                                label="Название"
                                name="name"
                                rules={[{required: true, message: 'Введите название игры'}]}
                            >
                                <Input/>
                            </Form.Item>
                            <Form.Item
                                label="Место"
                                name="place"
                                rules={[{required: true, message: 'Введите место проведения'}]}
                            >
                                <Input/>
                            </Form.Item>
                            <Form.Item
                                label="Дата и время"
                                name="datetime"
                                rules={[{message: 'Выберите дату и время'}]}
                            >
                                <DatePicker showTime/>
                            </Form.Item>
                            <Form.Item
                                label="Статус"
                                name="status"
                                rules={[{message: 'Выберите статус'}]}
                            >
                                <Select>
                                    <Option value={1}>Статус 1</Option>
                                    <Option value={2}>Статус 2</Option>
                                    <Option value={3}>Статус 3</Option>
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Уровень"
                                name="level"
                                rules={[{message: 'Выберите уровень'}]}
                            >
                                <Select>
                                    <Option value={1}>Уровень 1</Option>
                                    <Option value={2}>Уровень 2</Option>
                                    <Option value={3}>Уровень 3</Option>
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Команда 1"
                                name="team_1"
                                rules={[{message: 'Выберите команду 1'}]}
                            >
                                <Select>
                                    {teams.map(team => (
                                        <Option key={team.id} value={team.id}>{team.name}</Option>
                                    ))}
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Команда 2"
                                name="team_2"
                                rules={[{message: 'Выберите команду 2'}]}
                            >
                                <Select>
                                    {teams.map(team => (
                                        <Option key={team.id} value={team.id}>{team.name}</Option>
                                    ))}
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Задонатить автору"
                                name="amount"
                                rules={[{message: 'Введите стоимость'}]}
                            >
                                <Input type="number" min={0} max={1000}/>
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit">Изменить</Button>
                            </Form.Item>
                        </Form>
                    </Modal>
                    <Modal
                        title="Добавить игру"
                        open={addGameModalVisible}
                        onCancel={() => setAddGameModalVisible(false)}
                        footer={null}
                    >
                        <Form onFinish={handleAddGameSubmit}>
                            <Form.Item
                                label="Название"
                                name="name"
                                rules={[{required: true, message: 'Введите название игры'}]}
                            >
                                <Input/>
                            </Form.Item>
                            <Form.Item
                                label="Место"
                                name="place"
                                rules={[{required: true, message: 'Введите место проведения'}]}
                            >
                                <Input/>
                            </Form.Item>
                            <Form.Item
                                label="Дата и время"
                                name="datetime"
                                rules={[{required: true, message: 'Выберите дату и время'}]}
                            >
                                <DatePicker showTime/>
                            </Form.Item>
                            <Form.Item
                                label="Статус"
                                name="status"
                                rules={[{required: true, message: 'Выберите статус'}]}
                            >
                                <Select>
                                    <Option value={1}>Статус 1</Option>
                                    <Option value={2}>Статус 2</Option>
                                    <Option value={3}>Статус 3</Option>
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Уровень"
                                name="level"
                                rules={[{required: true, message: 'Выберите уровень'}]}
                            >
                                <Select>
                                    <Option value={1}>Уровень 1</Option>
                                    <Option value={2}>Уровень 2</Option>
                                    <Option value={3}>Уровень 3</Option>
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Команда 1"
                                name="team_1"
                                rules={[{required: true, message: 'Выберите команду 1'}]}
                            >
                                <Select>
                                    {teams.map(team => (
                                        <Option key={team.id} value={team.id}>{team.name}</Option>
                                    ))}
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Команда 2"
                                name="team_2"
                                rules={[{required: true, message: 'Выберите команду 2'}]}
                            >
                                <Select>
                                    {teams.map(team => (
                                        <Option key={team.id} value={team.id}>{team.name}</Option>
                                    ))}
                                </Select>
                            </Form.Item>
                            <Form.Item
                                label="Задонатить автору"
                                name="amount"
                                rules={[{required: true, message: 'Введите стоимость'}]}
                            >
                                <Input type="number" min={0} max={1000}/>
                            </Form.Item>
                            <Form.Item>
                                <Button type="primary" htmlType="submit">Добавить</Button>
                            </Form.Item>
                        </Form>
                    </Modal>
                    <Button style={{
                        marginTop: 10,
                    }}
                            type="primary" onClick={handleAddGame}>Добавить игру</Button>

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

export default MyGames;
