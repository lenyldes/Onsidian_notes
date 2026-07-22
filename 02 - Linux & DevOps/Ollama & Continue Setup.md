---
title: Ollama & Continue VSCode Setup
type: notes
tags:
  - ollama
  - docker
  - continue
  - ai
  - vscode
  - devops
created: 2026-07-22
---

# Ollama & Continue Extension — Локальные ИИ-модели

Инструкция по развертыванию локального Ollama сервер в Docker и его интеграции с расширением Continue в VSCode/IDE.

---

## 🐋 Запуск Ollama в Docker

### 1. Запуск контейнера Ollama
```bash
docker run -d \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  --name ollama \
  ollama/ollama
```

### 2. Загрузка и запуск модели (Qwen 2.5 Coder)
```bash
docker exec -it ollama ollama run qwen2.5-coder:1.5b
```

---

## ⚙️ Конфигурация для Continue (VSCode / JetBrains)

Скопируйте следующий YAML-конфиг в файлы настроек расширения **Continue** (`config.yaml` / `config.json`):

```yaml
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
