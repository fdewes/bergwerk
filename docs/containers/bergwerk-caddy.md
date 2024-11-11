# Bergwerk Caddy

The **Bergwerk Caddy container** is responsible for managing all external connections to the Bergwerk application. It provides various endpoints for accessing different components of the system:

### Available Endpoints

- **/** - HTML server for testing the chatbot through the Botfront Rasa Webchat Plugin. This endpoint is useful for development but may be disabled in production environments.
- **/wiki/** - Accesses the Bergwerk wiki, where chatbot content is stored and managed.
- **/api/** - Provides access to the Bergwerk API, facilitating data management and import/export operations.
- **/socketio/** - The SocketIO endpoint for the Rasa Webchat Plugin, enabling real-time communication between the frontend chat interface and the backend.

### SSL Configuration

If you’ve specified a `SERVER` name in the `config.env` file, Caddy will automatically request an SSL certificate via **Let’s Encrypt**. This setup ensures secure connections to your chatbot, enhancing data security for production deployments.

By managing external access and SSL provisioning, the Caddy service helps maintain a secure, organized structure for interacting with Bergwerk components.

## Caddyfile

```
--8<-- "bergwerk-caddy/Caddyfile"
```