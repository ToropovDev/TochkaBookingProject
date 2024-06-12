import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import axios from 'axios';

const EditTeamModal = ({ visible, team, onClose, onUpdate }) => {
    const [form] = Form.useForm();

    useEffect(() => {
        if (team) {
            form.setFieldsValue({
                opposite: team.opposite,
                outside_1: team.outside_1,
                outside_2: team.outside_2,
                setter: team.setter,
                middle_1: team.middle_1,
                middle_2: team.middle_2,
                libero: team.libero,
            });
        }
    }, [team, form]);

    const handleSubmit = async (values) => {
        try {
            await axios.patch(`http://localhost:8000/teams/${team.id}`, values, {
                withCredentials: true,
            });
            message.success('Команда успешно обновлена');
        } catch (error) {
            message.error('Не удалось обновить команду');
            console.error('Error:', error);
        }
    };

    return (
        <Modal
            title="Редактировать команду"
            open={visible}
            onCancel={onClose}
            footer={null}
        >
            <Form form={form} onFinish={handleSubmit}>
                <Form.Item name="opposite" label="Диагональный">
                    <Input />
                </Form.Item>
                <Form.Item name="outside_1" label="Доигровщик 1">
                    <Input />
                </Form.Item>
                <Form.Item name="outside_2" label="Доигровщик 2">
                    <Input />
                </Form.Item>
                <Form.Item name="setter" label="Связующий">
                    <Input />
                </Form.Item>
                <Form.Item name="middle_1" label="Центральный 1">
                    <Input />
                </Form.Item>
                <Form.Item name="middle_2" label="Центральный 2">
                    <Input />
                </Form.Item>
                <Form.Item name="libero" label="Либеро">
                    <Input />
                </Form.Item>
                <Form.Item>
                    <Button type="primary" htmlType="submit">Сохранить</Button>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default EditTeamModal;
