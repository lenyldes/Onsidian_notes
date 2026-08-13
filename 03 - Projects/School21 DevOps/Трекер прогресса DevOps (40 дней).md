---
title: Трекер прогресса DevOps (School 21) — План на 40 дней
type: project
tags:
  - devops
  - school21
  - project
  - tracker
created: 2026-08-13
---

# 🎯 Трекер прогресса DevOps (School 21) — 40-дневный интенсив

Заметка для отслеживания изучения и выполнения 5 проектов DevOps-линейки Школы 21 (**DO7 – DO11**).

---

## 📊 Сводный статус и метрики

* **Дата старта работы**: `2026-08-17` (Понедельник)
* **Целевой финиш (интенсив 4–8 ч/день)**: `~2026-09-14` (Понедельник)
* **Крайний дедлайн (40 дней)**: `2026-09-21` (Понедельник)
* **Запланированная нагрузка**: 4–8 часов в день
* **Связанная теория и материалы**: [[DevOps Tutor — Linux & Инфраструктура]], [[Linux & Системное администрирование]]

### 📈 Прогресс по проектам

| Проект | Описание | Планируемые даты | Статус | P2P Сдача |
| :--- | :--- | :--- | :---: | :---: |
| **DO7** | Docker Compose, Vagrant, Swarm | 17.08 – 21.08 | 🟡 В ожидании | ◻️ |
| **DO8** | Ansible & Consul Service Discovery | 22.08 – 27.08 | 🟡 В ожидании | ◻️ |
| **DO9** | Monitoring (Prometheus, Grafana, Loki) | 28.08 – 02.09 | 🟡 В ожидании | ◻️ |
| **DO10** | Basic Kubernetes (Minikube) | 03.09 – 08.09 | 🟡 В ожидании | ◻️ |
| **DO11** | Advanced K8s (k3s, Ingress, Cert-Manager) | 09.09 – 14.09 | 🟡 В ожидании | ◻️ |

---

## 🛠️ Подготовительный этап (13.08 – 16.08)

- [ ] **13.08 (Чт)**: Проверить аппаратную виртуализацию на ПК, установку Docker, Vagrant и VirtualBox/KVM.
- [ ] **14.08 (Пт)**: Клонировать репозитории проектов `DO7`–`DO11` из GitLab Школы 21.
- [ ] **15.08 (Сб)**: Проверить работоспособность Postman и коллекций тестов.
- [ ] **16.08 (Вс)**: Отдых перед началом интенсивного спринта.

---

## 📅 Пошаговый календарный чек-лист

### 🔹 Блок 1: DO7 — Docker Compose & Docker Swarm (17.08 – 21.08)

- [ ] **День 1 (17.08, Пн)**: Написать `Dockerfile` для микросервисов. Оптимизировать слои, измерить и записать размеры образов.
- [ ] **День 2 (18.08, Вт)**: Написать `docker-compose.yml`, пробросить порты `gateway` и `session`. Прогнать Postman-тесты локально.
- [ ] **День 3 (19.08, Ср)**: Создать 3 ВМ в Vagrant (`manager01`, `worker01`, `worker02`). Написать shell-скрипты автоматической установки Docker и Swarm.
- [ ] **День 4 (20.08, Чт)**: Загрузить образы на Docker Hub, развернуть стек в Swarm с Nginx Overlay Proxy. Настроить Portainer.
- [ ] **День 5 (21.08, Пт)**: Финализировать `REPORT.MD`, пройти Postman-тесты, сдать проект **DO7** на P2P.

---

### 🔹 Блок 2: DO8 — Automation Tools: Ansible & Consul (22.08 – 27.08)

- [ ] **День 6 (22.08, Сб)**: Vagrant (3 ВМ: `manager`, `node01`, `node02`), безпарольный SSH, инвентарь Ansible, проверка `ping`.
- [ ] **День 7 (23.08, Вс)**: Написать плейбук установки Docker/Compose и развертывания приложения. Выполнить Postman-тесты.
- [ ] **День 8 (24.08, Пн)**: Сформировать 3 роли Ansible (`application` на node01, `apache` + `postgres` на node02). Проверить записи БД и Apache.
- [ ] **День 9 (25.08, Вт)**: Consul Service Discovery: создать 4 ВМ (`consul_server`, `api`, `manager`, `db`). Подготовить `consul_server.hcl` и `consul_client.hcl`.
- [ ] **День 10 (26.08, Ср)**: Написать роли Ansible (`install_consul_server`, `install_consul_client`, `install_db`, `install_hotels_service`).
- [ ] **День 11 (27.08, Чт)**: Проверить CRUD операции `hotels_service` через Consul UI & Envoy. Финализировать `REPORT.MD` и сдать **DO8** на P2P.

---

### 🔹 Блок 3: DO9 — Monitoring: Prometheus, Grafana, Loki (28.08 – 02.09)

- [ ] **День 12 (28.08, Пт)**: Внедрить метрики Micrometer в Java-код приложения (RabbitMQ, bookings, gateway, auth).
- [ ] **День 13 (29.08, Сб)**: Интегрировать логи Loki. Поднять мониторинг-стек (Prometheus, Loki, node_exporter, cAdvisor, blackbox_exporter).
- [ ] **День 14 (30.08, Вс)**: Развернуть Grafana. Настроить дашборды инфраструктуры (ноды, контейнеры, CPU, RAM).
- [ ] **День 15 (31.08, Пн)**: Настроить дашборды прикладных метрик, доступности google.com и логов Loki в Grafana.
- [ ] **День 16 (01.09, Вт)**: Развернуть Alertmanager. Настроить алерты (RAM < 100MB, RAM > 1GB, CPU > 10%) и отправку в Telegram / Email.
- [ ] **День 17 (02.09, Ср)**: Сделать скриншоты алертов и панелей. Оформить `REPORT.MD` и сдать **DO9** на P2P.

---

### 🔹 Блок 4: DO10 — Basic Kubernetes: Minikube (03.09 – 08.09)

- [ ] **День 18 (03.09, Чт)**: Запустить Minikube (4 GB RAM), применить пример из `/src/example`, проверить `minikube dashboard` и `minikube service`.
- [ ] **День 19 (04.09, Пт)**: Написать YAML-манифесты ConfigMaps и Secrets (пароли БД, auth-ключи в base64).
- [ ] **День 20 (05.09, Сб)**: Написать манифесты Pods и Services для Postgres, RabbitMQ и 7 сервисов приложения.
- [ ] **День 21 (06.09, Вс)**: Применить манифесты (`kubectl apply`), проверить статусы (`kubectl get/describe/logs`), пробросить туннели и прогнать Postman.
- [ ] **День 22 (07.09, Пн)**: Сделать скриншоты K8s Dashboard. Изменить `pom.xml`, измерить и сравнить время редеплоя (`Recreate` vs `Rolling`).
- [ ] **День 23 (08.09, Вт)**: Заполнить `REPORT.MD` и сдать **DO10** на P2P.

---

### 🔹 Блок 5: DO11 — Advanced Kubernetes: k3s Cluster (09.09 – 14.09)

- [ ] **День 24 (09.09, Ср)**: Подготовить 3 ВМ, установить k3s без Traefik (`--disable=traefik`), объединить кластер по `NODE_TOKEN`.
- [ ] **День 25 (10.09, Чт)**: Установить Nginx Ingress Controller из официальных манифестов GitHub.
- [ ] **День 26 (11.09, Пт)**: Настроить `cert-manager` и запустить выпуск Wildcard SSL сертификата под свой домен.
- [ ] **День 27 (12.09, Сб)**: Настроить Ingress ресурс, создать Persistent Volume (PV/PVC) для PostgreSQL, развернуть приложение.
- [ ] **День 28 (13.09, Вс)**: Прогнать Postman-тесты по HTTPS через Ingress. Установить Prometheus Operator (`kubectl get pods -n monitoring`).
- [ ] **День 29 (14.09, Пн)**: Завершить `REPORT.MD`, пройти финальную P2P-сдачу проекта **DO11**.

---

## 📌 Заметки и полезные ссылки

* **Каталог выполнения**: `/home/lenyldes/Plan_DO_Task/`
* **Официальная документация**:
  * [Docker Compose Docs](https://docs.docker.com/compose/)
  * [Ansible Documentation](https://docs.ansible.com/)
  * [Consul Service Discovery](https://developer.hashicorp.com/consul)
  * [Prometheus Documentation](https://prometheus.io/docs/)
  * [Kubernetes Documentation](https://kubernetes.io/docs/)
