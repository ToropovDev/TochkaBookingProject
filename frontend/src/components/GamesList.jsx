import React, {useEffect, useState} from 'react';
import {Button, Card, DatePicker, Form, Input, message, Modal, Select, Space} from 'antd';
import axios from 'axios';
import GameDetailsModal from './GameDetailsModal';
import {useNavigate} from 'react-router-dom';

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

const GamesList = () => {
    const [games, setGames] = useState([]);
    const [modalVisible, setModalVisible] = useState(false);
    const [selectedGame, setSelectedGame] = useState(null);
    const [team1, setTeam1] = useState(null);
    const [team2, setTeam2] = useState(null);
    const [user1, setUser1] = useState(null);
    const [user2, setUser2] = useState(null);
    const [addGameModalVisible, setAddGameModalVisible] = useState(false);
    const [teams, setTeams] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchGames = async () => {
            try {
                const response = await axios.get('http://localhost:8000/games');
                setGames(response.data.data);
            } catch (error) {
                message.error('Failed to fetch games');
                console.error('Error:', error);
            }
        };

        const fetchTeams = async () => {
            try {
                const response = await axios.get('http://localhost:8000/teams');
                setTeams(response.data.data);
            } catch (error) {
                message.error('Failed to fetch teams');
                console.error('Error:', error);
            }
        };

        fetchGames();
        fetchTeams();
    }, []);

    const fetchTeam = async (teamId) => {
        try {
            const response = await axios.get(`http://localhost:8000/teams/${teamId}/`, {
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
            const response = await axios.get(`http://localhost:8000/user/${userId}/`, {
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
            const response = await axios.get(`http://localhost:8000/games/${gameId}/`, {
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
            const add_response = await axios.post(`http://localhost:8000/games/?${params.toString()}`, {}, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded", // Установим правильный заголовок Content-Type
                },
                withCredentials: true,
            });
            message.success('Игра успешно добавлена');
            setAddGameModalVisible(false);
            // Обновим список игр
            const response = await axios.get('http://localhost:8000/games');
            setGames(response.data.data);

            if (values.amount !== 0) {
                showModal(add_response.data.data);
            }
        } catch (error) {
            message.error('Не удалось добавить игру');
            console.error('Error:', error);
        }
    };

    return (
        <Space
            direction="vertical"
            size="middle"
            style={{
                display: 'flex',
            }}
        >

            {games.map((game) => (
                <Card key={game.id}
                                title={game.name}
                                style={{width: 300}}>
                    <div style={{display: 'flex', justifyContent: 'space-between'}}>
                        <div>
                            <p style={{fontSize: 12}}>
                                <b>Место:</b> {game.place}
                            </p>
                            <p style={{fontSize: 12}}>
                                <b>Дата</b> {formatDate(game.datetime)} {formatTime(game.datetime)}
                            </p>
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
            <Button type="primary" onClick={handleAddGame}>Добавить игру</Button>
        </Space>
    );
};

export default GamesList;
