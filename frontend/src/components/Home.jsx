import React from 'react';
import {Button, ConfigProvider, Space} from 'antd';
import {TinyColor} from "@ctrl/tinycolor";

import {useNavigate} from "react-router-dom";


const colors = ['#40e495', '#30dd8a', '#2bb673'];
const getHoverColors = (colors) =>
    colors.map((color) => new TinyColor(color).lighten(5).toString());
const getActiveColors = (colors) =>
    colors.map((color) => new TinyColor(color).darken(5).toString());

const Home = () => {
    const navigate = useNavigate();

    const onClick = () => {
        navigate('/login');
    };

    return (
        <Space>
            <ConfigProvider
                theme={{
                    components: {
                        Button: {
                            colorPrimary: `linear-gradient(135deg, ${colors.join(', ')})`,
                            colorPrimaryHover: `linear-gradient(135deg, ${getHoverColors(colors).join(', ')})`,
                            colorPrimaryActive: `linear-gradient(135deg, ${getActiveColors(colors).join(', ')})`,
                            lineWidth: 0,
                        },
                    },
                }}>
                <Button type="primary" size="large" onClick={onClick}>
                    Начать
                </Button>

            </ConfigProvider>
        </Space>
    );
};
export default Home;