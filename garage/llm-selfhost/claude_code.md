# CodeWhale + Deepseek
self-host deepseek api for codewhale
## Trail-1
### 1.1 model api
```
- [] Deepseek-V4-Flash
    - vllm ... --enable-auto-tool-choice --tool-call-parser deepseek_v4 --kv-cache-dtype fp8
    - resouce consumption: 
        - model weights: 148.66G 
        - --max-model-len 1048576
        - H20-96G x 4 -> 6x max concurrency
        - H20-96G x 2
```

### 1.2 deploy codewhale

```bash
# based on https://github.com/anthropics/claude-code/blob/main/.devcontainer/Dockerfile
docker pull node:20-slim

# https://code.claude.com/docs/en/quickstart
# within docker, install with npm
npm install -g @anthropic-ai/claude-code
```

```bash
export ANTHROPIC_BASE_URL="http://127.0.0.1:8000" 
export ANTHROPIC_API_KEY="fakekey" 
export ANTHROPIC_AUTH_TOKEN="any-value" 
export ANTHROPIC_DEFAULT_SONNET_MODEL="served_model_name" 
export ANTHROPIC_DEFAULT_OPUS_MODEL="served_model_name" 
export ANTHROPIC_DEFAULT_HAIKU_MODEL="served_model_name"
export CLAUDE_HOME="/path/to/your/claude/home"
claude

```

### 1.3 test record
- test okay
![alt text](images/claude_test.png)