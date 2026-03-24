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
