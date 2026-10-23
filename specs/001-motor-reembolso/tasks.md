# Tasks — Motor de Cálculo de Reembolso

> Cada task é pequena o bastante para virar **um commit**. Se você não consegue
> descrever o critério de aceite como "o teste X passa", a task está grande demais.
>
> Marque `[x]` conforme conclui — ao longo do caminho, não tudo no fim. O histórico
> de quando cada task foi marcada é lido na correção.

**Formato do commit:** `feat(T-003): <descrição>` · `test(T-003): <descrição>`

---

## Fase 1 — Fundação

- [x] **T-001** — Esqueleto do projeto (`pyproject.toml`, pacote `reembolso`, entry point CLI vazio)
  - **Atende:** critérios de aceite seção 9 (CLI existe)
  - **Aceite:** `reembolso --help` executa sem erro após `pip install -e .`
  - **Commit:** `9746013`

- [x] **T-002** — Leitura e escrita JSON (`io/json_io.py`) + modelo de lote
  - **Atende:** entrada/saída spec §4
  - **Aceite:** `test_io_le_lote_exemplo` passa carregando `exemplos/despesas-exemplo.json`
  - **Commit:** `aa7e442`

- [x] **T-003** — Função pura `calcular_lote` retornando um item por despesa (valores zerados)
  - **Atende:** schema de saída
  - **Aceite:** `test_calcular_lote_retorna_mesmos_ids` passa
  - **Commit:** `82d76e9` (núcleo completo de regras no mesmo commit, além do esqueleto zerado)

## Fase 2 — Regras de negócio (pré-limites)

- [x] **T-004** — Normalização de categoria
  - **Atende:** RN-009, AMB-010
  - **Aceite:** `test_AMB_010_categoria_maiuscula` (d-014) passa
  - **Commit:** `8c98b56`

- [x] **T-005** — Categoria fora da política
  - **Atende:** RN-009, AMB-009
  - **Aceite:** `test_RN_009_coworking_recusado` (d-005) passa
  - **Commit:** `58b002c`

- [x] **T-006** — Competência do período
  - **Atende:** RN-007, AMB-006
  - **Aceite:** `test_RN_007_fora_competencia` (d-008) passa
  - **Commit:** `ccdaf99`

- [x] **T-007** — Detecção de duplicatas
  - **Atende:** RN-008, AMB-005
  - **Aceite:** `test_RN_008_duplicata_segunda_recusada` (d-006/d-007) passa
  - **Commit:** `3b884c5`

- [x] **T-008** — Nota fiscal acima de R$ 100
  - **Atende:** RN-005, AMB-003
  - **Aceite:** `test_RN_005_nf_100_exato_ok` e `test_RN_005_nf_100_01_recusa` (d-003/d-004) passam
  - **Commit:** `e5a85c5`

- [x] **T-009** — Estorno (valor negativo)
  - **Atende:** RN-010, AMB-007
  - **Aceite:** `test_RN_010_estorno_zero_e_devolve_saldo` (d-009) passa
  - **Commit:** `ef4d1f8`

## Fase 3 — Limites e viagem

- [x] **T-010** — Pré-processamento “em viagem” a partir de hospedagem
  - **Atende:** RN-006, AMB-004
  - **Aceite:** `test_AMB_004_datas_viagem_de_hospedagem` passa
  - **Commit:** `038fad4`

- [x] **T-011** — Limite diário alimentação com saldo compartilhado
  - **Atende:** RN-001, RN-004, RN-012, AMB-001, AMB-002
  - **Aceite:** `test_RN_001_d001_d002_limite_60` passa
  - **Commit:** `5dbba42`

- [x] **T-012** — Limite diário transporte urbano
  - **Atende:** RN-002
  - **Aceite:** `test_RN_002_limite_transporte_80` passa
  - **Commit:** `300e1fd`

- [x] **T-013** — Hospedagem rateada por diárias
  - **Atende:** RN-003, AMB-008
  - **Aceite:** `test_RN_003_hospedagem_d010_rateio` passa
  - **Commit:** `d60118f`

- [x] **T-014** — Limites ampliados em viagem (+50%)
  - **Atende:** RN-006
  - **Aceite:** `test_RN_006_alimentacao_90_em_viagem` passa
  - **Commit:** `ef26033`

## Fase 4 — Saída e CLI

- [x] **T-015** — Arredondamento e status (`aprovado` / `parcial` / `recusado`)
  - **Atende:** RN-011, RN-004
  - **Aceite:** `test_RN_011_arredondamento_d011` passa
  - **Commit:** `898e81e`

- [x] **T-016** — Resumo (`total_informado`, `total_reembolsavel`)
  - **Atende:** spec §4 resumo
  - **Aceite:** `test_resumo_soma_itens` passa
  - **Commit:** `d2f3cb0`

- [x] **T-017** — CLI `calcular --input --output`
  - **Atende:** critérios de aceite seção 9
  - **Aceite:** `test_cli_calcular_arquivo` passa
  - **Commit:** `614903b`

- [x] **T-018** — Integração com `exemplos/despesas-exemplo.json`
  - **Atende:** critérios de aceite seção 9 (d-001…d-014)
  - **Aceite:** `test_exemplo_completo_ids_criticos` passa
  - **Commit:** `d0ed763`

---

## Fase 5 — Envelope (Política v4)

- [x] **T-019** — Modelo `Politica` + leitura `politica-v4.json` (`io/politica_io.py`)
  - **Atende:** RN-015, RN-005 (limiar), RN-006 (% viagem)
  - **Aceite:** `test_io_le_politica_envelope` passa *(coberto por fixtures de sessão)*
  - **Commit:** `6bec477`

- [x] **T-020** — Tabela de câmbio + retrocesso de data (AMB-016)
  - **Atende:** RN-013, AMB-016, AMB-017
  - **Aceite:** `test_RN_013_conversao_eur` passa
  - **Commit:** `6bec477`

- [x] **T-021** — Motor: mapa efetivo CC, categorias condicionais, limite 0 hospedagem
  - **Atende:** RN-003, RN-009, RN-014, AMB-013…015
  - **Aceite:** `test_envelope_cc_desconhecido` passa
  - **Commit:** `56e0451`

- [x] **T-022** — Entrada `moeda`; NF e limites em BRL
  - **Atende:** RN-013, RN-005, AMB-018, AMB-019
  - **Aceite:** `test_envelope_cc_comercial` (e-005, e-006) passa
  - **Commit:** `56e0451`

- [x] **T-023** — CLI `--politica` e `--cambio`
  - **Atende:** critérios aceite §9 v2
  - **Aceite:** `test_cli_calcular_arquivo` passa
  - **Commit:** `56e0451`

- [x] **T-024** — Regressão `despesas-exemplo.json` com CC-ENG-PLATAFORMA
  - **Atende:** RN-001, RN-003 (hospedagem bloqueada)
  - **Aceite:** `test_exemplo_completo_ids_criticos` passa
  - **Commit:** `f3d1fd6`

- [x] **T-025** — Documentação envelope: `docs(spec)`, `DECISIONS` D-001, `plan`, README
  - **Atende:** rastreabilidade Dia 2
  - **Aceite:** spec v2 + D-001 preenchido
  - **Commit:** `f23119c`, `01fd542`, `f3d1fd6` (README/sessão)

- [x] **T-026** — Fila de aprovação manual (RN-016, item C)
  - **Atende:** RN-016, AMB-020
  - **Aceite:** `test_RN_016_*` e e-007 `pendente` em `test_envelope_cc_comercial`
  - **Commit:** *(ver git)*

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
| RN-013 | T-020, T-022 | `test_RN_013_conversao_eur` |
| RN-014 | T-021 | `test_envelope_cc_comercial` (e-001) |
| RN-015 | T-019, T-021 | `test_envelope_cc_desconhecido` |
| AMB-013…019 | T-019…T-022 | testes envelope / RN-013 |
| RN-016 | T-026 | `test_RN_016_pendente_*`, `test_envelope_cc_comercial` (e-007) |
| AMB-020 | T-026 | `test_RN_016_pendente_acima_500` (limiar exato) |
