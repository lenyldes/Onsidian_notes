## Серверы
### Настройка fail2ban
#### Установка
```
sudo apt update && sudo apt install fail2ban
```
#### Проверка что все установилось
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
