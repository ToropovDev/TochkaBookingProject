import React, {useState} from 'react';
import {Button, Form, message, Modal, Select} from 'antd';
import axios from 'axios';

const {Option} = Select;

const positions = [
    {key: 0, label: 'Диагональный'},
    {key: 1, label: 'Доигровщик 1'},
    {key: 2, label: 'Доигровщик 2'},
    {key: 3, label: 'Связующий'},
    {key: 4, label: 'Центральный 1'},
    {key: 5, label: 'Центральный 2'},
    {key: 6, label: 'Либеро'}
];

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

// eslint-disable-next-line react/prop-types
const GameDetailsModal = ({visible, game, team1, team2, user1, user2, onClose}) => {
    const [isJoinFormVisible, setJoinFormVisible] = useState(false);
    const [selectedTeamId, setSelectedTeamId] = useState(null);
    const [selectedPosition, setSelectedPosition] = useState(null);

    const handleJoinClick = (teamId) => {
        setSelectedTeamId(teamId);
        setJoinFormVisible(true);
    };

    const handleFormSubmit = async () => {
        try {
            await axios.post(`http://localhost:8000/teams/join/${selectedTeamId}?position=${selectedPosition}`, {}, {
                withCredentials: true
            });
            message.success('Вы успешно записались в команду!');
            setJoinFormVisible(false);
        } catch (error) {
            message.error('Не удалось записаться в команду.');
            console.error('Error:', error);
        }
    };

    return (
        <Modal
            {/* eslint-disable-next-line react/prop-types */}
            title={game && game.name}
            visible={visible}
            onCancel={onClose}
            footer={null}
        >
            {game && (
                <div>
                    <p><b>Место:</b> {game.place}</p>
                    <p><b>Дата:</b> {formatDate(game.datetime)} {formatTime(game.datetime)}</p>
                    <p><b>Название:</b> {game.name}</p>
                    <p><b>Команда 1:</b> <br/> Создана пользователем: {user1 ? user1.username : 'Загрузка...'}</p>
                    <p>1.
                        Диагональный: {team1 && team1.opposite === null ? "позиция свободна" : team1 && team1.opposite}</p>
                    <p>2. Доигровщик
                        1: {team1 && team1.outside_1 === null ? "позиция свободна" : team1 && team1.outside_1}</p>
                    <p>3. Доигровщик
                        2: {team1 && team1.outside_2 === null ? "позиция свободна" : team1 && team1.outside_2}</p>
                    <p>4. Связующий: {team1 && team1.setter === null ? "позиция свободна" : team1 && team1.setter}</p>
                    <p>5. Центральный
                        1: {team1 && team1.middle_1 === null ? "позиция свободна" : team1 && team1.middle_1}</p>
                    <p>6. Центральный
                        2: {team1 && team1.middle_2 === null ? "позиция свободна" : team1 && team1.middle_2}</p>
                    <p>7. Либеро: {team1 && team1.libero === null ? "позиция свободна" : team1 && team1.libero}</p>
                    <Button type="primary" onClick={() => handleJoinClick(team1.id)}>Записаться в команду 1</Button>
                    <p><b>Команда 2:</b> <br/> Создана пользователем: {user2 ? user2.username : 'Загрузка...'}</p>
                    <p>1.
                        Диагональный: {team2 && team2.opposite === null ? "позиция свободна" : team2 && team2.opposite}</p>
                    <p>2. Доигровщик
                        1: {team2 && team2.outside_1 === null ? "позиция свободна" : team2 && team2.outside_1}</p>
                    <p>3. Доигровщик
                        2: {team2 && team2.outside_2 === null ? "позиция свободна" : team2 && team2.outside_2}</p>
                    <p>4. Связующий: {team2 && team2.setter === null ? "позиция свободна" : team2 && team2.setter}</p>
                    <p>5. Центральный
                        1: {team2 && team2.middle_1 === null ? "позиция свободна" : team2 && team2.middle_1}</p>
                    <p>6. Центральный
                        2: {team2 && team2.middle_2 === null ? "позиция свободна" : team2 && team2.middle_2}</p>
                    <p>7. Либеро: {team2 && team2.libero === null ? "позиция свободна" : team2 && team2.libero}</p>
                    <Button type="primary" onClick={() => handleJoinClick(team2.id)}>Записаться в команду 2</Button>
                </div>
            )}
            <Modal
                title="Записаться в команду"
                open={isJoinFormVisible}
                onCancel={() => setJoinFormVisible(false)}
                onOk={handleFormSubmit}
            >
                <Form>
                    <Form.Item label="Выберите позицию">
                        <Select onChange={(value) => setSelectedPosition(value)}>
                            {positions.map(position => (
                                <Option key={position.key} value={position.key}>{position.label}</Option>
                            ))}
                        </Select>
                    </Form.Item>
                </Form>
            </Modal>
        </Modal>
    );
};

export default GameDetailsModal;
