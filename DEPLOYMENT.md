# Fly.io Deployment Guide

## Prerequisites
- Fly.io CLI installed ✓
- Fly.io account (sign up at https://fly.io)

## Deployment Steps

### 1. Login to Fly.io
```bash
fly auth login
```

### 2. Launch your app
```bash
fly launch
```
- When prompted, accept the detected `fly.toml` configuration
- Choose your app name (default: wahl-chatbot) or customize it
- Select a region (recommended: fra - Frankfurt for German users)
- Do NOT deploy yet when asked - we need to set secrets first

### 3. Set your OpenAI API Key
```bash
fly secrets set OPENAI_API_KEY=your_openai_api_key_here
```
Replace `your_openai_api_key_here` with your actual OpenAI API key.

### 4. Deploy your application
```bash
fly deploy
```

### 5. Open your app
```bash
fly open
```

## Monitoring & Management

### View logs
```bash
fly logs
```

### Check app status
```bash
fly status
```

### Scale your app
```bash
fly scale count 1  # Run 1 machine
```

### View app info
```bash
fly info
```

## Updating Your App

When you make changes to your code:

```bash
fly deploy
```

## Costs

- Your app uses auto-stop/auto-start machines
- min_machines_running = 0 (scales to zero when not in use)
- 1GB RAM, shared CPU
- Should fit within Fly.io's free tier

## Important Notes

1. **Environment Variables**: The OpenAI API key must be set as a secret (step 3)
2. **Frontend**: You'll need to update `frontend/app.js` to point to your Fly.io app URL instead of localhost
3. **HTTPS**: Fly.io automatically provides HTTPS for your app
4. **CORS**: Already configured in the Flask app to accept requests

## Frontend Configuration

After deployment, update the API URL in `frontend/app.js`:

```javascript
// Change from:
const API_URL = "http://127.0.0.1:5000/chat";

// To:
const API_URL = "https://your-app-name.fly.dev/chat";
```

Replace `your-app-name` with your actual Fly.io app name.

## Troubleshooting

### View detailed logs
```bash
fly logs -a wahl-chatbot
```

### SSH into your app
```bash
fly ssh console
```

### Restart your app
```bash
fly apps restart wahl-chatbot
```

### Check health
Visit: `https://your-app-name.fly.dev/health`
