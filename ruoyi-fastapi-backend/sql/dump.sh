#!/bin/bash

pg_dump -h localhost -p 5432 -U postgres -d assistant \
  -t 'public."ChatSession"' \
  -t 'public."User"' \
  -t 'public."KnowledgeFile"' \
  -t 'public."_prisma_migrations"' \
  -t 'public."agent_chat_messages"' \
  -t 'public."dishes"' \
  -f multi_tables_backup.sql
