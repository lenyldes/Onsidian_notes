---
title: "Миграция AmneziaWG (Docker) между серверами"
type: notes
tags:
  - amnezia
  - wireguard
  - vpn
  - docker
  - devops
  - linux
created: 2026-10-30
---

# 🛡️ Миграция AmneziaWG (Docker) между серверами

Инструкция по переносу контейнера **AmneziaWG** на новый сервер с сохранением приватных ключей сервера, параметров обфускации и всех существующих клиентов. 

При таком переносе и переключении DNS клиентские устройства продолжают подключаться автоматически без перевыпуска конфигураций и вмешательства пользователей.

---

## 📋 Что переносится

Вся конфигурация сервиса хранится внутри Docker-контейнера в каталоге `/opt/amnezia/awg/`:
- `awg0.conf` — параметры сервера, обфускация (Jc, Jmin, Jmax, S1, S2, H1-H4) и список всех пиров.
- `clientsTable` — база клиентов для мобильного/десктопного приложения Amnezia.
- `wireguard_server_private_key.key` — приватный ключ сервера.
- `wireguard_server_public_key.key` — публичный ключ сервера (к нему привязаны клиенты).
- `wireguard_psk.key` — pre-shared ключ.

---

## 🚀 Пошаговый регламент миграции

### Шаг 1. Создание бэкапа на старом сервере

Подключитесь по SSH к **старому** серверу:

```bash
# 1. Проверяем точное имя контейнера и порт (например, amnezia-awg2 и порт 42209/udp)
docker ps

# 2. Копируем директорию awg из контейнера во временный каталог хоста
sudo docker cp amnezia-awg2:/opt/amnezia/awg /tmp/amnezia_awg_backup

# 3. Упаковываем в архив в домашней директории текущего пользователя
sudo tar -czvf ~/amnezia_awg_backup.tar.gz -C /tmp amnezia_awg_backup

# 4. Выставляем права на архив текущему пользователю
sudo chown $USER:$USER ~/amnezia_awg_backup.tar.gz

# 5. Удаляем временную папку
sudo rm -rf /tmp/amnezia_awg_backup
```

---

### Шаг 2. Передача архива на новый сервер

Выберите наиболее удобный способ:

#### Вариант А: Прямая передача со старого сервера на новый (выполняется на старом сервере)
```bash
scp -P <SSH_PORT_NEW> ~/amnezia_awg_backup.tar.gz <USER_NEW>@<IP_NEW>:~/
```

#### Вариант Б: Загрузка новым сервером со старого (выполняется на новом сервере)
```bash
scp -P <SSH_PORT_OLD> <USER_OLD>@<IP_OLD>:~/amnezia_awg_backup.tar.gz ~/
```

#### Вариант В: Передача через локальную машину (в один пайп без сохранения на Mac)
Выполняется на вашем локальном компьютере:
```bash
ssh -p <SSH_PORT_OLD> <USER_OLD>@<IP_OLD> "cat ~/amnezia_awg_backup.tar.gz" | \
  ssh -p <SSH_PORT_NEW> <USER_NEW>@<IP_NEW> "cat > ~/amnezia_awg_backup.tar.gz"
```

---

### Шаг 3. Подготовка нового сервера через приложение

1. В приложении Amnezia добавьте **новый сервер** по IP и SSH-реквизитам.
2. Запустите установку протокола **AmneziaWG**.
3. **Критически важно:** укажите **тот же UDP-порт**, что был на старом сервере (например, `42209`).
4. Дождитесь успешного завершения развертывания контейнера.

---

### Шаг 4. Восстановление конфигурации на новом сервере

Подключитесь по SSH к **новому** серверу:

```bash
# 1. Распаковываем архив в текущую папку (флаг -xzvf)
tar -xzvf amnezia_awg_backup.tar.gz

# 2. Выдаем полные права на распакованные файлы (обязательно для обхода прав демона)
sudo chmod -R 777 ./amnezia_awg_backup

# 3. Останавливаем контейнер
sudo docker stop amnezia-awg2

# 4. Копируем файлы внутрь контейнера (обратите внимание на /. в конце источника)
sudo docker cp ./amnezia_awg_backup/. amnezia-awg2:/opt/amnezia/awg/

# 5. Запускаем контейнер
sudo docker start amnezia-awg2

# 6. Удаляем бэкапы с хоста
rm -rf ./amnezia_awg_backup amnezia_awg_backup.tar.gz
```

---

### Шаг 5. Проверка статуса и пиров

```bash
# Проверка пиров и статуса WireGuard интерфейса
sudo docker exec amnezia-awg2 awg show

# Просмотр последних строк логов контейнера
sudo docker logs amnezia-awg2 --tail 25
```

> [!TIP]
> В выводе команды `awg show` должны присутствовать все клиенты (`peer: <публичный_ключ>`), которые были на старом сервере.

---

### Шаг 6. Переключение DNS

1. В панели управления DNS обновите **A-запись** вашего домена на IP-адрес нового сервера.
2. После обновления DNS-кэша все устройства автоматически начнут туннелировать трафик через новый сервер.

---

## ⚠️ Частые ошибки и их решения

1. **`tar (child): ... Cannot open: Permission denied`**:
   - Причина: попытка сохранить архив в `/tmp` без достаточных прав или поверх файла с чужими правами.
   - Решение: сохранять архив прямо в домашнюю папку пользователя `~/amnezia_awg_backup.tar.gz` и выполнять `sudo chown $USER:$USER ~/amnezia_awg_backup.tar.gz`.

2. **`tar: Refusing to read archive contents from terminal (missing -f option?)`**:
   - Причина: опечатка в параметрах (`-xzvg` вместо `-xzvf`).
   - Решение: указывать ключ `-f` перед именем файла архива (`tar -xzvf ...`).

3. **`open ... awg0.conf: permission denied` / `unexpected EOF` при `docker cp`**:
   - Причина: у файлов `awg0.conf` и `clientsTable` выставлены строгие права доступа внутри архива.
   - Решение: перед копированием выполнить `sudo chmod -R 777 ./amnezia_awg_backup` и использовать команду с `sudo` и завершающей точкой: `sudo docker cp ./amnezia_awg_backup/. <container>:/opt/amnezia/awg/`.
