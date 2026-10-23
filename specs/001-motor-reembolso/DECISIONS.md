# Log de Decisões e Mudanças de Spec

> Uma entrada **toda vez** que a spec mudar. Este arquivo é a prova de que a spec
> foi tratada como artefato vivo e não como cerimônia de abertura.

Ordem cronológica inversa: a mais recente primeiro.

---

## D-002 — Política v4 (envelope Dia 2) · 2026-10-23

**Gatilho:** Envelope lacrado — Política de Reembolso v4 (centros de custo, moeda/câmbio).

**O que mudou na spec:** v1.0 → v2.0. Limites deixam de ser constantes (RN-001…003,
RN-006 parametrizados por arquivo externo e `centro_custo`). Novas RN-013 (câmbio),
RN-014 (representação), RN-015 (mapa efetivo CC). Entrada ganha `moeda` opcional;
CLI exige política e câmbio. Saída: `valor_reembolsavel` em BRL; NF sobre valor
convertido (AMB-018). Novas AMB-013…019. §10 “ignorar centro_custo” revogado.
Item C (aprovação > R$ 500) explicitamente fora de escopo.

**Por quê:** Comunicado do RH com vigência imediata; financeiro mantém política fora
do código; despesas internacionais exigem conversão antes dos tetos em BRL.

**O que isso invalidou:** Constantes fixas em `motor/politica.py`; assinatura
`calcular_lote(lote)` sem política/câmbio; CLI só `--input`/`--output`; aceites de
d-001/d-002/d-010/d-014 com limites globais R$ 60/250; RN-009 como lista fixa de
três categorias.

**Tasks afetadas:** T-003, T-011…T-014, T-017, T-018 (refatoração/regressão).
Novas: T-019…T-025 (Fase 5).

**Custo:** ~15 arquivos (spec, plan, tasks, io, motor, cli, tests, README, exemplos).

---

## D-001 — <título curto> · `<data>`

**Gatilho:**

**O que mudou na spec:**

**Por quê:**

**O que isso invalidou:**

**Tasks afetadas:**

**Custo:**
