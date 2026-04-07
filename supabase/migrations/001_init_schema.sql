-- ============================================
-- Supabase Schema for OpenClaw Agent Memory
-- Created: 2026-04-07
-- ============================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable vector extension for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- Phase 1: 強化記憶系統
-- ============================================

-- Agent Memory Table
CREATE TABLE IF NOT EXISTS agent_memory (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  session_key TEXT,
  memory_type TEXT CHECK (memory_type IN ('short_term', 'long_term', 'context', 'user_preference')),
  content TEXT NOT NULL,
  metadata JSONB DEFAULT '{}',
  embedding VECTOR(1536),  -- OpenAI embedding dimension
  importance INT DEFAULT 5 CHECK (importance >= 1 AND importance <= 10),
  tags TEXT[] DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Memory Topics Table
CREATE TABLE IF NOT EXISTS memory_topics (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  topic TEXT UNIQUE NOT NULL,
  summary TEXT,
  keywords TEXT[] DEFAULT '{}',
  importance INT DEFAULT 1 CHECK (importance >= 1 AND importance <= 10),
  access_count INT DEFAULT 0,
  last_accessed TIMESTAMPTZ DEFAULT NOW(),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX IF NOT EXISTS idx_agent_memory_session ON agent_memory(session_key);
CREATE INDEX IF NOT EXISTS idx_agent_memory_type ON agent_memory(memory_type);
CREATE INDEX IF NOT EXISTS idx_agent_memory_importance ON agent_memory(importance DESC);
CREATE INDEX IF NOT EXISTS idx_memory_topics_topic ON memory_topics(topic);

-- ============================================
-- Phase 2: 任務執行日誌
-- ============================================

CREATE TABLE IF NOT EXISTS task_logs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  task_type TEXT NOT NULL,
  task_name TEXT,
  status TEXT CHECK (status IN ('success', 'failed', 'timeout', 'running', 'cancelled')),
  payload JSONB DEFAULT '{}',
  result JSONB,
  error_message TEXT,
  error_details JSONB,
  duration_ms INT,
  agent_id TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_task_logs_type ON task_logs(task_type);
CREATE INDEX IF NOT EXISTS idx_task_logs_status ON task_logs(status);
CREATE INDEX IF NOT EXISTS idx_task_logs_created ON task_logs(created_at DESC);

-- ============================================
-- Phase 3: X 發文系統
-- ============================================

CREATE TABLE IF NOT EXISTS x_posts (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  scheduled_at TIMESTAMPTZ,
  posted_at TIMESTAMPTZ,
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'posted', 'failed', 'cancelled')),
  content_zh TEXT,
  content_jp TEXT,
  content_en TEXT,
  image_path TEXT,
  post_url TEXT,
  error_message TEXT,
  retry_count INT DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_x_posts_status ON x_posts(status);
CREATE INDEX IF NOT EXISTS idx_x_posts_scheduled ON x_posts(scheduled_at);

-- ============================================
-- Phase 4: 用戶設定中心
-- ============================================

CREATE TABLE IF NOT EXISTS user_settings (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  key TEXT UNIQUE NOT NULL,
  value JSONB NOT NULL,
  description TEXT,
  category TEXT DEFAULT 'general',
  is_encrypted BOOLEAN DEFAULT FALSE,
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_settings_key ON user_settings(key);
CREATE INDEX IF NOT EXISTS idx_user_settings_category ON user_settings(category);

-- ============================================
-- Utility Functions
-- ============================================

-- Auto-update updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables with updated_at
DROP TRIGGER IF EXISTS update_agent_memory_updated_at ON agent_memory;
CREATE TRIGGER update_agent_memory_updated_at
  BEFORE UPDATE ON agent_memory
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_memory_topics_updated_at ON memory_topics;
CREATE TRIGGER update_memory_topics_updated_at
  BEFORE UPDATE ON memory_topics
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_settings_updated_at ON user_settings;
CREATE TRIGGER update_user_settings_updated_at
  BEFORE UPDATE ON user_settings
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Row Level Security (RLS)
-- ============================================

-- Enable RLS
ALTER TABLE agent_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_topics ENABLE ROW LEVEL SECURITY;
ALTER TABLE task_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE x_posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_settings ENABLE ROW LEVEL SECURITY;

-- Policy: Allow all operations for authenticated users (service role bypasses RLS)
CREATE POLICY "Enable all for service role" ON agent_memory
  FOR ALL USING (true);

CREATE POLICY "Enable all for service role" ON memory_topics
  FOR ALL USING (true);

CREATE POLICY "Enable all for service role" ON task_logs
  FOR ALL USING (true);

CREATE POLICY "Enable all for service role" ON x_posts
  FOR ALL USING (true);

CREATE POLICY "Enable all for service role" ON user_settings
  FOR ALL USING (true);

-- ============================================
-- Vector Search Functions
-- ============================================

-- Simple similarity search function
CREATE OR REPLACE FUNCTION search_memory(
  query_embedding VECTOR(1536),
  match_threshold FLOAT DEFAULT 0.7,
  match_count INT DEFAULT 5
)
RETURNS TABLE(
  id UUID,
  content TEXT,
  memory_type TEXT,
  importance INT,
  similarity FLOAT
)
AS $$
BEGIN
  RETURN QUERY
  SELECT
    m.id,
    m.content,
    m.memory_type,
    m.importance,
    1 - (m.embedding <=> query_embedding) AS similarity
  FROM agent_memory m
  WHERE m.embedding IS NOT NULL
    AND 1 - (m.embedding <=> query_embedding) > match_threshold
  ORDER BY m.embedding <=> query_embedding
  LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Sample Data (for testing)
-- ============================================

-- Insert sample memory
INSERT INTO agent_memory (session_key, memory_type, content, importance, tags) VALUES
  ('test-session', 'user_preference', 'User prefers to be addressed in Traditional Chinese', 8, ARRAY['language', 'preference']),
  ('test-session', 'context', 'User is working on integrating Supabase with OpenClaw', 7, ARRAY['project', 'supabase']),
  ('test-session', 'long_term', 'User has a character named 牧原澪 (Makihara Mio) for X posting', 9, ARRAY['character', 'x-account']);
