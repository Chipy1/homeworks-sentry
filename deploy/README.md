# Развертывание self-hosted Sentry (компактная выжимка)

## Шаги

```bash
# 1. Официальный self-hosted (compose ~20+ сервисов: web, relay, snuba,
#    clickhouse, postgres, kafka, redis, symbolicator, ...)
git clone https://github.com/getsentry/self-hosted.git && cd self-hosted
git checkout 26.8.0

# 2. Конфиги: .env + docker-compose.override.yml из этой папки
cp ../deploy/.env ./.env
cp ../deploy/docker-compose.override.yml ./

# 3. Запуск
sudo ./install.sh   # образы, миграции БД, секреты
sudo docker compose up -d

# 4. Суперпользователь
sudo docker compose exec web /.venv/bin/sentry createuser \
  --email admin@local.dev --password '...' --superuser
```

## Файлы

| файл | роль |
|---|---|
| `docker-compose.override.yml` | добавляет MailHog для перехвата alert-писем |
| `.env` | pin релиза 26.8.0, `SENTRY_BIND=9000`, retention 90 дней |

## Почта (задача 3)

Админка Sentry -> options: `mail.host=mailhog`, `mail.port=1025`,
`mail.from=sentry@localhost`. События шлются на почту, письма видны в MailHog
на http://192.168.50.42:8025.
