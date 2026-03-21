***
**Docker:**

Установка:
```
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

Запуск:
```
docker exec -it ollama ollama run qwen2.5-coder:1.5b
```

Continue:
```
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: qwen2.5-coder:1.5b
    provider: ollama
    model: qwen2.5-coder:1.5b
    roles:
      - autocomplete
```

