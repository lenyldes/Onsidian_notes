## Серверы
### fail2ban
#### Установка и настройка
```
sudo apt update && sudo apt install fail2ban
```
##### Проверка что все установилось
```
sudo systemctl status fail2ban.service
```
#### Исправление ошибок
##### Have not found any log file for sshd jail
```
[30772]: ERROR   Failed during configuration: Have not found any log file for sshd jail
[30772]: ERROR   Async configuration of server failed
systemd[1]: **fail2ban.service: Main process exited, code=exited, status=255/EXCEPTION**
systemd[1]: **fail2ban.service: Failed with result 'exit-code'.**
```
Логи пишутся сюда:
```
sudo journalctl -u ssh | tail -20
```
Далее производим настройку:
```
sudo nano /etc/fail2ban/jail.d/sshd.conf
```
Сюда пишем:
```
[sshd]
maxretry = 3
bantime = 3600
findtime = 3600
```
Устанавливаем:
```
sudo apt install python3-systemd
```
Проверяем:
```
sudo systemctl restart fail2ban && sudo systemctl status fail2ban.service
```
#### Основные команды
```
# Список всех джейлов (активных)
sudo fail2ban-client status

# Подробный статус конкретного джейла
sudo fail2ban-client status sshd
```
```
# Посмотреть последние строки лога fail2ban
sudo tail -f /var/log/fail2ban.log

# Поиск ошибок в логе
sudo grep ERROR /var/log/fail2ban.log
```
