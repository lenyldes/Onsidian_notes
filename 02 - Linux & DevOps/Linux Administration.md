---
title: Linux & Server Administration
type: notes
tags:
  - linux
  - devops
  - docker
  - fail2ban
  - raspi5
  - warp
  - postgresql
created: 2026-07-22
---

# Linux & Системное администрирование

Коллекция заметок, инструкций и шпаргалок по настройке Linux-серверов, Docker, безопасности и утилит.

---

## 🐋 Docker & Docker Compose

### Часовой пояс в Docker Compose
Настройка часового пояса для контейнеров:
```yaml
environment:
  - TZ=Europe/Moscow
```

### PostgreSQL + DBeaver (CloudBeaver) в Docker Compose
Пример `docker-compose.yaml` для локального запуска PostgreSQL и веб-клиента CloudBeaver:

```yaml
services:
  postgres:
    image: postgres:18.1
    environment:
      - POSTGRES_PASSWORD="12345678"
    volumes:
      - pg_data:/var/lib/postgresql
    ports:
      - "5432:5432"
    
  dbeaver:
    image: dbeaver/cloudbeaver:25.3.5
    ports:
      - "8978:8978"
    volumes:
      - dbeaver_data:/opt/cloudebeaver/workspace

volumes:
  pg_data:
  dbeaver_data:
```

**Инструкция по подключению:**
1. Запуск: `docker compose up -d`
2. Веб-интерфейс доступен по адресу: `http://localhost:8978/`
3. Создайте администратора при первом входе.
4. **Важно при настройке подключения к БД:** поле **Host** меняем с `localhost` на имя сервиса Docker — `postgres`.
5. В настройках **Database List** включите флаг: `Show all databases`.

---

## 🛡️ Безопасность серверов: Fail2ban

### Установка и базовое включение
```bash
sudo apt update && sudo apt install fail2ban
sudo systemctl status fail2ban.service
```

### Настройка правил SSH (`sshd`)
Создайте или отредактируйте файл конфигурации `/etc/fail2ban/jail.d/sshd.conf`:
```ini
[sshd]
enabled = true
backend = systemd
maxretry = 3
bantime = 3600
findtime = 3600
```

### Устранение ошибки: "Have not found any log file for sshd jail"
Если в логах возникает ошибка:
```text
ERROR Failed during configuration: Have not found any log file for sshd jail
ERROR Async configuration of server failed
```

Проверьте логи SSH:
```bash
sudo journalctl -u ssh | tail -20
```

Установите пакет интеграции с systemd и перезапустите fail2ban:
```bash
sudo apt install python3-systemd
sudo systemctl restart fail2ban && sudo systemctl status fail2ban.service
```

### Основные команды Fail2ban
```bash
# Список всех активных джейлов
sudo fail2ban-client status

# Подробный статус джейла sshd
sudo fail2ban-client status sshd

# Мониторинг логов fail2ban
sudo tail -f /var/log/fail2ban.log

# Поиск ошибок в логе
sudo grep ERROR /var/log/fail2ban.log
```

---

## 🍓 Raspberry Pi 5: Охлаждение и вентилятор Kernel Control

Для настройки кулера на RPi 5 отредактируйте `/boot/firmware/config.txt`:
```bash
sudo nano /boot/firmware/config.txt
```

Добавьте в конец файла:
```ini
[all]
dtparam=nvme
dtparam=pciex1_gen=3
usb_max_current_enable=1

# Включить управление вентилятором через ядро
dtparam=cooling_fan=on
```

---

## ✈️ Telemt (Telegram Proxy)

### Генерация случайных ключей в hex
```bash
openssl rand -hex 16
```

Скрипт для массовой генерации ключей пользователя:
```bash
cat > generate_hex.sh << 'EOF'
#!/bin/bash

FILE="config.toml"

for i in {1..15}; do
    value=$(openssl rand -hex 16)
    echo "user${i} = \"${value}\"" >> "$FILE"
done
EOF

chmod +x generate_hex.sh
```

### Получение Proxy Config
```bash
sudo bash -c 'curl https://core.telegram.org/getProxyConfig > proxy-config-v4.txt'
sudo bash -c 'curl https://core.telegram.org/getProxyConfigV6 > proxy-config-v6.txt'

# Выдаем права на запись
sudo chmod a+w proxy-config-v4.txt 
sudo chmod a+w proxy-config-v6.txt 
```

### Настройка `config.toml`
```toml
[general]
use_middle_proxy = true
proxy_config_v4_cache_path = "/run/telemt/cache/proxy-config-v4.txt"
proxy_config_v6_cache_path = "/run/telemt/cache/proxy-config-v6.txt"
beobachten = false
```

### Изменения в `docker-compose.yaml`
```yaml
working_dir: /run/telemt
volumes:
  - ./config.toml:/run/telemt/config.toml:ro
  - ./proxy-config-v4.txt:/run/telemt/cache/proxy-config-v4.txt
  - ./proxy-config-v6.txt:/run/telemt/cache/proxy-config-v6.txt
```

### Обновление контейнера Telemt
```bash
docker compose down
docker rmi ghcr.io/telemt/telemt:latest
docker compose up -d && docker compose logs -f
```

---

## 🌐 Cloudflare WARP CLI

Установка и настройка WARP CLI для работы с сети/AGY:

```bash
# 1. Скачиваем ключи безопасности и добавляем официальный репозиторий Cloudflare
curl -fsSL https://pkg.cloudflareclient.com/pubkey.gpg | sudo gpg --yes --dearmor --output /usr/share/keyrings/cloudflare-warp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/cloudflare-warp-archive-keyring.gpg] https://pkg.cloudflareclient.com/ $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/cloudflare-client.list

# 2. Обновляем списки и устанавливаем клиент WARP
sudo apt-get update
sudo apt-get install cloudflare-warp -y

# 3. Регистрируем устройство (делается однократно)
warp-cli --accept-tos registration new

# 4. Включаем туннель
warp-cli connect
```
