# Server

This page covers server-side inference for Fish Audio S2, plus quick links for WebUI inference and Docker deployment.

## API Server Inference

Fish Speech provides an HTTP API server entrypoint at `tools/api_server.py`.

The server now also exposes an OpenAI-compatible speech synthesis route at `POST /v1/audio/speech`.
It also exposes `GET /v1/models` for OpenAI-compatible model discovery.

### Start the server locally

```bash
python tools/api_server.py \
  --device cpu \
  --llama-checkpoint-path checkpoints/s2-pro \
  --decoder-checkpoint-path checkpoints/s2-pro/codec.pth \
  --listen 0.0.0.0:8881
```

Common options:

- `--compile`: enable `torch.compile` optimization
- `--half`: use fp16 mode
- `--api-key`: require bearer token authentication
- `--workers`: set worker process count

### Health check

```bash
curl -X GET http://127.0.0.1:8881/v1/health
```

Expected response:

```json
{"status":"ok"}
```

### Main API endpoint

- `POST /v1/audio/speech` for OpenAI-compatible text-to-speech generation
- `GET /v1/models` for OpenAI-compatible TTS model listing
- `POST /v1/tts` for the native Fish Speech text-to-speech API
- `POST /v1/vqgan/encode` for VQ encode
- `POST /v1/vqgan/decode` for VQ decode

OpenAI-compatible request example:

```bash
curl -X POST http://127.0.0.1:8881/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello from Fish Speech.",
    "voice": "alloy",
    "response_format": "mp3"
  }' \
  --output speech.mp3
```

OpenAI-compatible model listing example:

```bash
curl -X GET http://127.0.0.1:8881/v1/models
```

Supported OpenAI-compatible response formats on `/v1/audio/speech`:

- `mp3`
- `opus`
- `aac`
- `flac`
- `wav`
- `pcm`

## WebUI Inference

For WebUI usage, see:

- [WebUI Inference](https://speech.fish.audio/inference/#webui-inference)

## Docker

For Docker-based server or WebUI deployment, see:

- [Docker Setup](https://speech.fish.audio/install/#docker-setup)

You can also start the server profile directly with Docker Compose:

```bash
docker compose --profile server up
```
