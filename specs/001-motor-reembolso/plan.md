# Plano Técnico — Motor de Cálculo de Reembolso

**Versão:** 1.1 · **Baseado na spec:** 2.0

> Aqui mora o COMO. Este arquivo pode e deve falar de linguagem, biblioteca e
> arquitetura. O que ele **não** pode é introduzir regra de negócio nova — se
> apareceu uma, ela pertence à `spec.md`.

---

## 1. Stack

| Escolha | O quê | Por quê | O que descartei e por quê |
|---|---|---|---|
| Linguagem | Python 3.11+ | Familiaridade, CLI rápida, ecossistema de testes maduro | Node/Go — válidos, mas Python acelera iteração no prazo de 2 dias |
| Testes | pytest | Fixtures, parametrização, nomes legíveis para rastreabilidade | unittest — mais verboso sem ganho |
| Parsing/validação | `json` (stdlib) + tipos/dataclasses | Entrada já é JSON estável; validação mínima conforme spec | pydantic — útil, mas dependência extra desnecessária no escopo |
| Aritmética monetária | `decimal.Decimal` (quantize 0.01) | Evita erro de ponto flutuante; alinha RN-011 | `float` — proibido para valores finais |
| CLI | `argparse` (stdlib) | Subcomando `calcular` com `--input` / `--output` | click/typer — dependência opcional |
| Lint/format | `ruff` (opcional) | Formatação e lint leves se houver tempo | — |

---

## 2. Arquitetura

```
entrada JSON
    → leitor (I/O)
    → parser → modelo DespesaLote
    → pré-processador (datas em viagem, duplicatas)
    → motor de regras (núcleo puro, sem I/O)
    → montador de saída
    → escritor JSON
```

**Fronteiras:**

- **Núcleo (`motor/`):** normalização, duplicata, competência, NF, limites diários,
  hospedagem, estorno, arredondamento. Entrada/saída são estruturas de dados simples
  (dicts ou dataclasses). Sem leitura de arquivo.
- **Borda (`cli/`, `io/`):** argparse, read/write UTF-8, código de saída de erro
  apenas para falha de I/O ou JSON inválido.

Essa separação permite testar cada RN com dicts pequenos e absorver mudanças do
Dia 2 alterando só o núcleo ou política em constantes.

---

## 3. Modelo de dados

**Entrada (interna):**

- `Colaborador(id, nome, centro_custo)`
- `Periodo(competencia, inicio, fim)` — `date`
- `Despesa(..., valor: Decimal, tem_nota_fiscal, moeda: str = "BRL")`
- `Politica` / `TabelaCambio` — carregados na borda, passados ao núcleo
- `Lote(colaborador, periodo, despesas: list[Despesa])` — ordem preservada

**Saída (interna):**

- `ResultadoItem(id, valor_informado, valor_reembolsavel, status, justificativa)`
- `ResultadoLote(colaborador_id, competencia, itens, resumo)`

**Estado de processamento (núcleo):**

- `SaldoDiario`: mapa `(date, categoria) → Decimal` restante
- `Viagem`: `set[date]` calculado uma vez
- `VistoDuplicata`: chave `(data, cat_norm, fornecedor, valor, descricao_norm)`

**Justificativa:** string construída pelo motor com códigos curtos internos traduzidos
para texto legível (ex.: `LIMITE_ALIMENTACAO`, `DUPLICATA`).

---

## 4. Como a política é representada

Arquivo JSON (`politica-v4.json`) → `Politica` em `motor/politica_config.py`
(`padrao`, `centros_custo`, limiar NF, % viagem). Resolução por
`mapa_efetivo(centro_custo)` conforme RN-015.

Câmbio: `cambio.json` → `TabelaCambio` (`motor/cambio.py`); leitura em
`io/cambio_io.py`.

Regex de diárias em `motor/hospedagem.py`: inalterada.

CLI obriga `--politica` e `--cambio`; núcleo permanece puro
(`calcular_lote(lote, politica, cambio)`).

---

## 5. Decisões técnicas

### DT-001 — Núcleo sem I/O

**Contexto:** Rastreabilidade e envelope exigem testes por RN.
**Decisão:** Função `calcular_lote(Lote, Politica, TabelaCambio) -> ResultadoLote` pura.
**Alternativa descartada:** CLI testada só com arquivos temporários — mais lenta e opaca.
**Consequência:** Testes unitários rápidos; CLI fina.

### DT-002 — Decimal end-to-end no núcleo

**Contexto:** d-011 e somas diárias.
**Decisão:** Parse de `valor` para `Decimal(str(...))`; quantize na borda de saída.
**Alternativa descartada:** Centavos inteiros — exige conversão na CLI e nos testes JSON.
**Consequência:** Testes comparam `Decimal` ou strings `"33.33"`.

### DT-003 — Pacote instalável com entry point

**Contexto:** Comando exigido `<comando> calcular ...`.
**Decisão:** `pyproject.toml` com script `reembolso = cli.main:main`.
**Alternativa descartada:** `python -m src` — funciona, mas README fica menos claro.
**Consequência:** `pip install -e .` then `reembolso calcular ...`.

---

## 6. Estratégia de testes

- **Nível:** ~85% unitário (núcleo por RN), ~15% integração (CLI + JSON exemplo).
- **Cada `RN-NNN` da spec tem teste?** Sim — arquivo `tests/test_rn_*.py` ou
  `tests/test_motor.py` com funções `test_RN_001_limite_diario_alimentacao_agregado`.
- **Casos de borda da seção 7:** parametrizados com ids `d-001`, `d-007`, etc.
- **AMB:** testes dedicados onde a decisão não é óbvia (AMB-003 fronteira 100,
  AMB-004 viagem, AMB-008 rateio hospedagem).
- **Nomenclatura:** prefixo `test_RN_XXX_` ou `test_AMB_XXX_` + descrição snake_case;
  fixtures em `tests/conftest.py` com factory `despesa(**kwargs)`.
- **Integração:** `tests/test_exemplo_completo.py` carrega `exemplos/despesas-exemplo.json`
  e asserta snapshot parcial (ids críticos) ou valores esperados documentados na task T-018.

---

## 7. Riscos

| Risco | Probabilidade | O que faço se acontecer |
|---|---|---|
| Envelope altera política | Alta (Dia 2) | Spec → DECISIONS → tasks Fase 5 → ajustar `politica.py` |
| Regex de diárias falha em descrição atípica | Média | Fallback N=1 documentado na spec; teste explícito |
| Ordem de regras gera divergência | Baixa | Testes de ordem d-001/d-002 e d-013/NF |
| Drift spec ↔ código | Média | Task bloqueia implementação sem RN na spec |

---

## 8. Layout de pastas

```
src/reembolso/
  __init__.py
  cli/main.py
  io/json_io.py
  motor/
    calcular.py
    politica_config.py
    cambio.py
    normalizacao.py
    duplicata.py
    viagem.py
    hospedagem.py
    limites.py
tests/
  conftest.py
  test_rn_*.py
  test_cli.py
  test_exemplo_completo.py
pyproject.toml
```
