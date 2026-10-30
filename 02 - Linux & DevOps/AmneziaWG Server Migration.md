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

# 3. Упаковываем архив прямо в домашнюю директорию текущего пользователя (НЕ в /tmp!)
sudo tar -czvf ~/amnezia_awg_backup.tar.gz -C /tmp amnezia_awg_backup

# 4. ОБЯЗАТЕЛЬНО меняем владельца архива на текущего пользователя
sudo chown $USER:$USER ~/amnezia_awg_backup.tar.gz

# 5. Удаляем временную папку
sudo rm -rf /tmp/amnezia_awg_backup
```

---

### Шаг 2. Передача архива на новый сервер

Выберите подходящий способ передачи:

#### Вариант А: Прямая передача со старого сервера на новый (выполняется на старом сервере)
```bash
scp -P <SSH_PORT_NEW> ~/amnezia_awg_backup.tar.gz <USER_NEW>@<IP_NEW>:~/
```

#### Вариант Б: Загрузка новым сервером со старого (выполняется на новом сервере)
```bash
scp -P <SSH_PORT_OLD> <USER_OLD>@<IP_OLD>:~/amnezia_awg_backup.tar.gz ~/
```

#### Вариант В: Передача через локальную машину (в один пайп без сохранения на диск Mac)
Выполняется в терминале вашего локального компьютера:
```bash
ssh -p <SSH_PORT_OLD> <USER_OLD>@<IP_OLD> "cat ~/amnezia_awg_backup.tar.gz" | \
  ssh -p <SSH_PORT_NEW> <USER_NEW>@<IP_NEW> "cat > ~/amnezia_awg_backup.tar.gz"
```

---

### Шаг 3. Подготовка нового сервера через приложение

1. В приложении Amnezia на телефоне/ПК добавьте **новый сервер** по IP и SSH-реквизитам.
2. Запустите установку протокола **AmneziaWG**.
3. **Критически важно:** укажите **тот же UDP-порт**, что был на старом сервере (например, `42209`).
4. Дождитесь успешного завершения развертывания чистого контейнера.

---

### Шаг 4. Восстановление конфигурации на новом сервере

Подключитесь по SSH к **новому** серверу (архив `amnezia_awg_backup.tar.gz` уже лежит в `~`):

```bash
# 1. Распаковываем архив (внимание: флаг -xzvf с буквой 'f', а не 'g')
tar -xzvf amnezia_awg_backup.tar.gz

# 2. КРИТИЧЕСКИ ВАЖНО: выдаем полные права на распакованные файлы,
#    так как у файлов конфига внутри архива стоят права доступа только для внутреннего UID контейнера:
sudo chmod -R 777 ./amnezia_awg_backup

# 3. Останавливаем контейнер
sudo docker stop amnezia-awg2

# 4. Копируем файлы внутрь контейнера через sudo (ОБЯЗАТЕЛЬНО точка /. на конце):
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

1. В панели управления DNS вашего домена обновите **A-запись** на IP-адрес нового сервера.
2. После обновления DNS-кэша все устройства автоматически начнут туннелировать трафик через новый сервер без перенастройки клиентов.

---

## ⚠️ Реальные ошибки при миграции, логи и их решения

### 1. Ошибка создания архива в `/tmp` (Permission denied)

**Симптомы / Лог ошибки:**
```text
lenyldes@r1072211:~
➜ sudo  tar -czvf /tmp/amnezia_awg_backup.tar.gz -C /tmp amnezia_awg_backup
amnezia_awg_backup/
amnezia_awg_backup/awg0.conf
amnezia_awg_backup/wireguard_psk.key
amnezia_awg_backup/clientsTable
amnezia_awg_backup/wireguard_server_public_key.key
amnezia_awg_backup/wireguard_server_private_key.key
tar (child): /tmp/amnezia_awg_backup.tar.gz: Cannot open: Permission denied
tar (child): Error is not recoverable: exiting now
tar: Child returned status 2
tar: Error is not recoverable: exiting now
```

- **Причина**: Ошибка `Cannot open: Permission denied` в каталоге `/tmp` обычно возникает, если файл с таким именем уже был ранее создан с другими правами (например, другим пользователем или root с ограниченными правами), либо у процесса сжатия `gzip` нет прав на запись в целевую точку `/tmp`.
- **Решение**: Сохранять архив прямо в домашнюю директорию текущего пользователя (`~`), после чего сразу изменить владельца архива:
  ```bash
  sudo tar -czvf ~/amnezia_awg_backup.tar.gz -C /tmp amnezia_awg_backup
  sudo chown $USER:$USER ~/amnezia_awg_backup.tar.gz
  ```
  После этого архив гарантированно читается и скачивается через `scp` без необходимости вызывать `sudo`.

---

### 2. Опечатка в опциях `tar` (missing -f option)

**Симптомы / Лог ошибки:**
```text
lenyldes@ubuntu24:~$ ls
amnezia_awg_backup.tar.gz
lenyldes@ubuntu24:~$ tar -xzvg amnezia_awg_backup.tar.gz 
tar: Refusing to read archive contents from terminal (missing -f option?)
tar: Error is not recoverable: exiting now
```

- **Причина**: В команде опечатка — указана буква **`g`** вместо **`f`** (`-xzvg` вместо `-xzvf`). Ключ `-f` (file) указывает имя архива, с которым нужно работать. Без ключа `-f` утилита `tar` считает имя файла отдельным аргументом и пытается прочитать архив прямо со стандартного ввода (терминала), поэтому завершается с ошибкой.
- **Решение**: Использовать корректную букву **`f`**:
  ```bash
  tar -xzvf amnezia_awg_backup.tar.gz
  ```

---

### 3. Ошибка прав при `docker cp` и unexpected EOF

**Симптомы / Лог ошибки:**
```text
lenyldes@ubuntu24:~$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                                             NAMES
59123a14a231   amnezia-awg2   "dumb-init /opt/amne…"   4 minutes ago   Up 4 minutes   0.0.0.0:42209->42209/udp, [::]:42209->42209/udp   amnezia-awg2
lenyldes@ubuntu24:~$ docker stop amnezia-awg2 
amnezia-awg2
lenyldes@ubuntu24:~$ docker cp ./amnezia_awg_backup/ amnezia-awg2:/opt/amnezia/awg/
time="2026-10-06T14:48:50Z" level=error msg="Can't add file /home/lenyldes/amnezia_awg_backup/awg0.conf to tar: open /home/lenyldes/amnezia_awg_backup/awg0.conf: permission denied"
time="2026-10-06T14:48:50Z" level=error msg="Can't add file /home/lenyldes/amnezia_awg_backup/clientsTable to tar: archive/tar: missed writing 2032 bytes"
time="2026-10-06T14:48:50Z" level=error msg="Can't add file /home/lenyldes/amnezia_awg_backup/wireguard_psk.key to tar: archive/tar: missed writing 2032 bytes"
time="2026-10-06T14:48:50Z" level=error msg="Can't add file /home/lenyldes/amnezia_awg_backup/wireguard_server_private_key.key to tar: archive/tar: missed writing 2032 bytes"
time="2026-10-06T14:48:50Z" level=error msg="Can't add file /home/lenyldes/amnezia_awg_backup/wireguard_server_public_key.key to tar: archive/tar: missed writing 2032 bytes"
time="2026-10-06T14:48:50Z" level=error msg="Can't close tar writer: archive/tar: missed writing 2032 bytes"
Successfully copied 5.58kB (transferred 1.02kB) to amnezia-awg2:/opt/amnezia/awg/
Error response from daemon: unexpected EOF
```

- **Причина**: Файлы `awg0.conf` и `clientsTable` создаются процессом Amnezia внутри контейнера со строгими масками прав (`---------x`, UID 1001). При распаковке архива на хосте обычный пользователь не имеет прав на чтение этих файлов (`open ...: permission denied`). Команда `docker cp` под капотом пытается упаковать эти файлы в потоковый tar и передать демону Docker, натыкается на отказ в доступе и падает с `unexpected EOF`. Кроме того, путь без завершающей точки `./amnezia_awg_backup/` создаёт лишний вложенный каталог внутри контейнера.
- **Решение**:
  1. Выдать полные права на распакованные файлы перед копированием:
     ```bash
     sudo chmod -R 777 ./amnezia_awg_backup
     ```
  2. Выполнить копирование под `sudo` с завершающей точкой `/.` (копировать содержимое, а не папку):
     ```bash
     sudo docker cp ./amnezia_awg_backup/. amnezia-awg2:/opt/amnezia/awg/
     ```
  3. Запустить контейнер:
     ```bash
     sudo docker start amnezia-awg2
     ```
