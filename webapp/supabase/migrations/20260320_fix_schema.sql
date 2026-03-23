-- Criar tabelas de aprendizado se não existirem
CREATE TABLE IF NOT EXISTS performance_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid,
  post_id text,
  tema text,
  tipo text,
  estilo_copy text,
  likes integer DEFAULT 0,
  salvamentos integer DEFAULT 0,
  ctr float DEFAULT 0.0,
  created_at timestamptz DEFAULT now()
);

CREATE TABLE IF NOT EXISTS preferred_models (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid,
  tipo text,
  conteudo text,
  created_at timestamptz DEFAULT now()
);

-- Desativar RLS temporariamente para testes sem login
ALTER TABLE chats DISABLE ROW LEVEL SECURITY;
ALTER TABLE messages DISABLE ROW LEVEL SECURITY;
ALTER TABLE performance_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE preferred_models DISABLE ROW LEVEL SECURITY;

-- Remover a exigência de que o usuário exista na tabela auth.users para podermos testar livremente
ALTER TABLE chats DROP CONSTRAINT IF EXISTS chats_user_id_fkey;
ALTER TABLE messages DROP CONSTRAINT IF EXISTS messages_user_id_fkey;
ALTER TABLE performance_logs DROP CONSTRAINT IF EXISTS performance_logs_user_id_fkey;
ALTER TABLE preferred_models DROP CONSTRAINT IF EXISTS preferred_models_user_id_fkey;
ALTER TABLE vault_items DROP CONSTRAINT IF EXISTS vault_items_user_id_fkey;
ALTER TABLE user_settings DROP CONSTRAINT IF EXISTS user_settings_user_id_fkey;
ALTER TABLE integrations DROP CONSTRAINT IF EXISTS integrations_user_id_fkey;
