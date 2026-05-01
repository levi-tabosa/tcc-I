-- 1. ENABLE EXTENSIONS
-- Required for fast ILIKE searches (Trigram)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- 2. CORE PERFORMANCE INDEXES
-- Index for Home Page (Last 12 Months) - Speeds up numeric filtering
CREATE INDEX IF NOT EXISTS idx_despesas_ano_mes 
ON camara.deputados_despesas (ano, mes);

-- Composite Index for Rankings and Statistics
-- Covering mandato_id and valor_documento allows "Index Only Scans" (no table hit)
CREATE INDEX IF NOT EXISTS idx_despesas_mandato_id_valor 
ON camara.deputados_despesas (mandato_id, valor_documento);

-- Index for Deputy Name Searches
-- Speeds up ILIKE '%name%' queries in emendas and proposições
CREATE INDEX IF NOT EXISTS idx_deputados_nome_civil_trgm 
ON camara.deputados USING gin (nome_civil gin_trgm_ops);

-- 3. FUNCTIONAL INDEXES (Complex Logic)
-- Index for Supplier Normalization
-- This must EXACTLY match the logic used in your Python router and summary scripts
CREATE INDEX IF NOT EXISTS idx_fornecedor_normalizado
ON camara.deputados_despesas (
    upper(trim(regexp_replace(nome_fornecedor, '\s+(S/A|S\.A\.|SA|LTDA|EIRELI|ME|EPP|EI|LIMITADA).*$', '', 'gi')))
);

-- Index for CNPJ detection
-- Helps the summary generator filter between CPF and CNPJ instantly
CREATE INDEX IF NOT EXISTS idx_despesas_cnpj_len
ON camara.deputados_despesas (
    (length(regexp_replace(cnpj_cpf_fornecedor, '[^0-9]', '', 'g')) > 11)
);

-- 4. SUMMARY TABLE INTEGRITY
-- Ensure primary keys exist for the summary tables to prevent duplicates
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'summary_empresas_geral_pkey') THEN
        ALTER TABLE camara.summary_empresas_geral ADD PRIMARY KEY (legislatura_id);
    END IF;
END $$;

-- 5. STATISTICS UPDATE
-- Tells the PostgreSQL Query Planner about the new data distribution
ANALYZE camara.deputados;
ANALYZE camara.deputados_mandatos;
ANALYZE camara.deputados_despesas;
ANALYZE camara.summary_empresas_geral;

-- Verify (Optional)
SELECT
    relname AS table_name,
    indexrelname AS index_name,
    idx_scan AS number_of_scans
FROM pg_stat_user_indexes
WHERE schemaname = 'camara'
ORDER BY idx_scan DESC;