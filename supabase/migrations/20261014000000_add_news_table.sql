CREATE TABLE IF NOT EXISTS news (
  id           uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
  date         date        NOT NULL,
  headline     text        NOT NULL,
  body         text        NOT NULL,
  product_tags text[]      NOT NULL DEFAULT '{}',
  company_tags text[]      NOT NULL DEFAULT '{}',
  event_type   text        NOT NULL DEFAULT 'other',
  source_url   text        NOT NULL DEFAULT '',
  created_at   timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE news ENABLE ROW LEVEL SECURITY;

CREATE POLICY "news_read_authenticated"
  ON news FOR SELECT TO authenticated
  USING (true);

CREATE POLICY "news_write_admin"
  ON news FOR ALL TO authenticated
  USING (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
  )
  WITH CHECK (
    EXISTS (SELECT 1 FROM profiles WHERE id = auth.uid() AND role = 'admin')
  );
