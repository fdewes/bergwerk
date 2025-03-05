 # Bergwerk SocketIO

This file is responsible for building the container for the **SocketIO adapter**. The SocketIO adapter facilitates real-time communication between the **Rasa Webchat Plugin** (located in the Caddy root directory, `index.html`) and the **Bergwerk API**.

The adapter acts as a bridge, enabling data flow and interaction between the web-based chat interface and the backend API.

## docker-compose.yaml

```Dockerfile
--8<-- "api/Dockerfile"
```