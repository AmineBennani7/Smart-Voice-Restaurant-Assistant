import React from 'react';
import { Modal, Button, Form } from 'react-bootstrap';

const ChangePasswordModal = ({ show, handleClose, handlePasswordChange, oldPassword, setOldPassword, newPassword, setNewPassword }) => (
    <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
            <Modal.Title>Cambiar contraseña</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            <Form onSubmit={handlePasswordChange}>
                <Form.Group controlId="formOldPassword">
                    <Form.Label>Contraseña actual</Form.Label>
                    <Form.Control type="password" placeholder="Actual contraseña" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} />
                </Form.Group>
                <Form.Group controlId="formNewPassword">
                    <Form.Label>Nueva contraseña</Form.Label>
                    <Form.Control type="password" placeholder="Nueva contraseña" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} />
                </Form.Group>
                <Button variant="primary" type="submit">
                    Guardar
                </Button>
            </Form>
        </Modal.Body>
    </Modal>
);

export default ChangePasswordModal;
