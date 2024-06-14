import React, {useEffect, useState} from 'react';
import {useParams} from 'react-router-dom';
import axios from 'axios';
import {Card, message} from 'antd';
import UrlAddr from "../Url/UrlAddr.js";

function GameDetails() {
    const {gameId} = useParams();
    const [gameDetails, setGameDetails] = useState(null);

    useEffect(() => {
        const fetchGameDetails = async () => {
            try {
                const response = await axios.get(UrlAddr + `/games/${gameId}`);
                setGameDetails(response.data);
            } catch (error) {
                message.error('Failed to fetch game details');
                console.error('Error:', error);
            }
        };

        fetchGameDetails();
    }, [gameId]);

    if (!gameDetails) {
        return null;
    }

    return (
        <Card title={gameDetails.name}>
            <p><b>Место:</b> {gameDetails.place}</p>
            <p><b>Дата:</b> {gameDetails.datetime}</p>
            <p><b>Стоимость:</b> {gameDetails.amount} руб.</p>
        </Card>
    );
}

export default GameDetails;
