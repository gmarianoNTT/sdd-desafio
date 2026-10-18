# Tasks — Motor de Cálculo de Reembolso

> Cada task é pequena o bastante para virar **um commit**. Se você não consegue
> descrever o critério de aceite como "o teste X passa", a task está grande demais.
>
> Marque `[x]` conforme conclui — ao longo do caminho, não tudo no fim. O histórico
> de quando cada task foi marcada é lido na correção.

**Formato do commit:** `feat(T-003): <descrição>` · `test(T-003): <descrição>`

---

## Fase 1 — Fundação

- [ ] **T-001** — Esqueleto do projeto (`pyproject.toml`, pacote `reembolso`, entry point CLI vazio)
  - **Atende:** critérios de aceite seção 9 (CLI existe)
  - **Aceite:** `reembolso --help` executa sem erro após `pip install -e .`
  - **Commit:**

- [ ] **T-002** — Leitura e escrita JSON (`io/json_io.py`) + modelo de lote
  - **Atende:** entrada/saída spec §4
  - **Aceite:** `test_io_le_lote_exemplo` passa carregando `exemplos/despesas-exemplo.json`
  - **Commit:**

- [ ] **T-003** — Função pura `calcular_lote` retornando um item por despesa (valores zerados)
  - **Atende:** schema de saída
  - **Aceite:** `test_calcular_lote_retorna_mesmos_ids` passa
  - **Commit:**

## Fase 2 — Regras de negócio (pré-limites)

- [ ] **T-004** — Normalização de categoria
  - **Atende:** RN-009, AMB-010
  - **Aceite:** `test_AMB_010_categoria_maiuscula` (d-014) passa
  - **Commit:**

- [ ] **T-005** — Categoria fora da política
  - **Atende:** RN-009, AMB-009
  - **Aceite:** `test_RN_009_coworking_recusado` (d-005) passa
  - **Commit:**

- [ ] **T-006** — Competência do período
  - **Atende:** RN-007, AMB-006
  - **Aceite:** `test_RN_007_fora_competencia` (d-008) passa
  - **Commit:**

- [ ] **T-007** — Detecção de duplicatas
  - **Atende:** RN-008, AMB-005
  - **Aceite:** `test_RN_008_duplicata_segunda_recusada` (d-006/d-007) passa
  - **Commit:**

- [ ] **T-008** — Nota fiscal acima de R$ 100
  - **Atende:** RN-005, AMB-003
  - **Aceite:** `test_RN_005_nf_100_exato_ok` e `test_RN_005_nf_100_01_recusa` (d-003/d-004) passam
  - **Commit:**

- [ ] **T-009** — Estorno (valor negativo)
  - **Atende:** RN-010, AMB-007
  - **Aceite:** `test_RN_010_estorno_zero_e_devolve_saldo` (d-009) passa
  - **Commit:**

## Fase 3 — Limites e viagem

- [ ] **T-010** — Pré-processamento “em viagem” a partir de hospedagem
  - **Atende:** RN-006, AMB-004
  - **Aceite:** `test_AMB_004_datas_viagem_de_hospedagem` passa
  - **Commit:**

- [ ] **T-011** — Limite diário alimentação com saldo compartilhado
  - **Atende:** RN-001, RN-004, RN-012, AMB-001, AMB-002
  - **Aceite:** `test_RN_001_d001_d002_limite_60` passa
  - **Commit:**

- [ ] **T-012** — Limite diário transporte urbano
  - **Atende:** RN-002
  - **Aceite:** `test_RN_002_limite_transporte_80` passa
  - **Commit:**

- [ ] **T-013** — Hospedagem rateada por diárias
  - **Atende:** RN-003, AMB-008
  - **Aceite:** `test_RN_003_hospedagem_d010_rateio` passa
  - **Commit:**

- [ ] **T-014** — Limites ampliados em viagem (+50%)
  - **Atende:** RN-006
  - **Aceite:** `test_RN_006_alimentacao_90_em_viagem` passa
  - **Commit:**

## Fase 4 — Saída e CLI

- [ ] **T-015** — Arredondamento e status (`aprovado` / `parcial` / `recusado`)
  - **Atende:** RN-011, RN-004
  - **Aceite:** `test_RN_011_arredondamento_d011` passa
  - **Commit:**

- [ ] **T-016** — Resumo (`total_informado`, `total_reembolsavel`)
  - **Atende:** spec §4 resumo
  - **Aceite:** `test_resumo_soma_itens` passa
  - **Commit:**

- [ ] **T-017** — CLI `calcular --input --output`
  - **Atende:** critérios de aceite seção 9
  - **Aceite:** `test_cli_calcular_arquivo` passa
  - **Commit:**

- [ ] **T-018** — Integração com `exemplos/despesas-exemplo.json`
  - **Atende:** critérios de aceite seção 9 (d-001…d-014)
  - **Aceite:** `test_exemplo_completo_ids_criticos` passa
  - **Commit:**

---

## Fase 5 — Envelope (criar no Dia 2)

<Novas tasks a partir da mudança de requisito. Numeração continua de T-019.>

---

## Cobertura

| Regra da spec | Task | Teste |
|---|---|---|
| RN-001 | T-011 | `test_RN_001_d001_d002_limite_60` |
| RN-002 | T-012 | `test_RN_002_limite_transporte_80` |
| RN-003 | T-013 | `test_RN_003_hospedagem_d010_rateio` |
| RN-004 | T-011, T-015 | `test_RN_001_d001_d002_limite_60` |
| RN-005 | T-008 | `test_RN_005_nf_100_exato_ok`, `test_RN_005_nf_100_01_recusa` |
| RN-006 | T-010, T-014 | `test_RN_006_alimentacao_90_em_viagem` |
| RN-007 | T-006 | `test_RN_007_fora_competencia` |
| RN-008 | T-007 | `test_RN_008_duplicata_segunda_recusada` |
| RN-009 | T-004, T-005 | `test_RN_009_coworking_recusado` |
| RN-010 | T-009 | `test_RN_010_estorno_zero_e_devolve_saldo` |
| RN-011 | T-015 | `test_RN_011_arredondamento_d011` |
| RN-012 | T-011 | `test_RN_001_d001_d002_limite_60` |
| AMB-001 | T-011 | `test_RN_001_d001_d002_limite_60` |
| AMB-002 | T-011 | `test_RN_001_d001_d002_limite_60` |
| AMB-003 | T-008 | `test_RN_005_nf_100_01_recusa` |
| AMB-004 | T-010 | `test_AMB_004_datas_viagem_de_hospedagem` |
| AMB-005 | T-007 | `test_RN_008_duplicata_segunda_recusada` |
| AMB-006 | T-006 | `test_RN_007_fora_competencia` |
| AMB-007 | T-009 | `test_RN_010_estorno_zero_e_devolve_saldo` |
| AMB-008 | T-013 | `test_RN_003_hospedagem_d010_rateio` |
| AMB-009 | T-005 | `test_RN_009_coworking_recusado` |
| AMB-010 | T-004 | `test_AMB_010_categoria_maiuscula` |
| AMB-011 | T-015 | `test_RN_011_arredondamento_d011` |
| AMB-012 | T-011 | coberto indiretamente em T-018 (`d-012`) |
