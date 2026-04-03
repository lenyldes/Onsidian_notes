## Docker

### docker-compose.yaml

Установка времени:
```bash
    environment:
      - TZ=Europe/Moscow
```

## Серверы
### fail2ban
#### Установка и настройка
``` bash
sudo apt update && sudo apt install fail2ban
```
##### Проверка что все установилось
``` bash
sudo systemctl status fail2ban.service
```
##### Уменьшаем таймауты

``` bash
sudo nano /etc/fail2ban/jail.d/sshd.conf
```
Сюда пишем:
``` bash
[sshd]
maxretry = 3
bantime = 3600
findtime = 3600
```
#### Исправление ошибок
##### Have not found any log file for sshd jail
``` bash
[30772]: ERROR   Failed during configuration: Have not found any log file for sshd jail
[30772]: ERROR   Async configuration of server failed
systemd[1]: **fail2ban.service: Main process exited, code=exited, status=255/EXCEPTION**
systemd[1]: **fail2ban.service: Failed with result 'exit-code'.**
```
Логи пишутся сюда:
``` bash
sudo journalctl -u ssh | tail -20
```
Далее производим настройку:
``` bash
sudo nano /etc/fail2ban/jail.d/sshd.conf
```
Сюда пишем (дописываем):
``` bash
[sshd]
maxretry = 3
bantime = 3600
findtime = 3600
enabled = true
backend = systemd
```
Устанавливаем:
``` bash
sudo apt install python3-systemd
```
Проверяем:
``` bash
sudo systemctl restart fail2ban && sudo systemctl status fail2ban.service
```
#### Основные команды
``` bash
# Список всех джейлов (активных)
sudo fail2ban-client status

# Подробный статус конкретного джейла
sudo fail2ban-client status sshd
```
``` bash
# Посмотреть последние строки лога fail2ban
sudo tail -f /var/log/fail2ban.log

# Поиск ошибок в логе
sudo grep ERROR /var/log/fail2ban.log
```

### Кулер Pi5

```bash
sudo nano /boot/firmware/config.txt
```

И добавить в конец:

```bash
**[all]**
dtparam=nvme
dtparam=pciex1_gen=3
usb_max_current_enable=1

# Включить управление вентилятором через ядро
dtparam=cooling_fan=on
```
^^ не помогло
### Telemt

```bash
openssl rand -hex 16
```

```bash
#!/bin/bash

# Имя целевого файла
FILE="config.toml"

# Цикл для 10 записей
for i in {1..15}; do
    # Генерируем случайную 16-байтовую hex-строку
    value=$(openssl rand -hex 16)
    # Дописываем строку в файл
    echo "user${i} = \"${value}\"" >> "$FILE"

done
```

1) Необходимо получить proxy-config
```bash
sudo bash -c 'curl https://core.telegram.org/getProxyConfig > proxy-config-v4.txt'
sudo bash -c 'curl https://core.telegram.org/getProxyConfigV6 > proxy-config-v6.txt'
# флаг -c - выполнить команду в строке

# выдаем права на запись
sudo chmod a+w proxy-config-v4.txt 
sudo chmod a+w proxy-config-v6.txt 
```
2) Добавить зависимости в config.toml
```bash
# === General Settings ===
[general]
use_middle_proxy = true
proxy_config_v4_cache_path = "/run/telemt/cache/proxy-config-v4.txt"
proxy_config_v6_cache_path = "/run/telemt/cache/proxy-config-v6.txt"
beobachten = false # тоже отключаем, тк идут ошибки от него
```
А также в docker-compose.yaml
```bash
    working_dir: /run/telemt
    volumes:
      - ./config.toml:/run/telemt/config.toml:ro
      - ./proxy-config-v4.txt:/run/telemt/cache/proxy-config-v4.txt
      - ./proxy-config-v6.txt:/run/telemt/cache/proxy-config-v6.txt
```


Обновление
```bash
docker compose down
docker rmi ghcr.io/telemt/telemt:latest
docker compose up -d && docker compose logs -f
```


### SQL используя Docker Compose

```
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

docker compose up -d

Заходим: http://localhost:8978/
Создаем пользователя

**!!!Далее при подключении!!!**:
HOST с localhost меняем на имя сервиса, т.е. postgres
В настройках DATABASE LIST: v Show all databases

#### AmneziaClient на сервер

Для Debian

