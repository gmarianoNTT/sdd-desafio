# CHECKLIST.md Dia 1 implementation
_Exported on 10/23/2026 at 20:39:48 GMT-3 from Cursor (3.15.6)_

---

**User**

Com referencia no arquivo CHECKLIST.md analise as atividades Dia 1 — manhã (documentação antes de código) e implemente as que conseguir. Faça os commits de acordo com as regras do desafio.
Em seguida resuma o que executou e diga quais não conseguiu executar e o porque.
Em seguida atualize o @CHECKLIST.md  conforme atividades executadas.


---

**Cursor**

Analisando o CHECKLIST e a documentação do projeto para implementar as atividades da manhã do Dia 1.


Redigindo a documentação completa (spec, plan e tasks) com decisões de negócio defensáveis alinhadas ao JSON de exemplo.


## Resumo — Dia 1 manhã

### Executado

**`spec.md` (v1.0)** — commit `29b9049`
- Problema, objetivo e fora de escopo
- Schema de entrada/saída com exemplo JSON
- **RN-001 a RN-012** ligadas à política do RH
- **12 ambiguidades (AMB-001 a AMB-012)** com citação, leituras, decisão e justificativa
- Casos de borda alinhados a d-001…d-014
- Critérios de aceite verificáveis, sem vazamento técnico
- Ordem de aplicação das regras

**`plan.md` (v1.0)** — commit `a8361c1`
- Stack: Python 3.11+, pytest, `Decimal`, argparse, layout `src/reembolso/`
- Arquitetura núcleo vs I/O, modelo de dados, política em constantes
- DT-001 a DT-003 com alternativas descartadas
- Estratégia de testes por RN/AMB

**`tasks.md`** — commit `7518556`
- **T-001 a T-018** com Atende/Aceite
- Matriz de cobertura RN/AMB ↔ task ↔ teste

**Extra (pré-requisito):** `CLAUDE.md` atualizado no commit do plan

**Sessão:** `docs/sessions/02-dia1-manha-documentacao.md` — commit `50f0bc8`

**`CHECKLIST.md`** atualizado localmente (arquivo ignorado pelo git)

---

### Não executado (e por quê)

| Item | Motivo |
|------|--------|
| **Fork público** | Ação sua no GitHub; não dá para confirmar daqui |
| **`/export` nativo Claude Code → `01-…md`** | Sessão no **Cursor**; já existe `preparacao-ambiente.md`. Sessão 02 foi export alternativo (FAQ) |
| **Anotação formal item a item do JSON** | Decisões foram incorporadas na spec (seção 7 + AMB), sem arquivo de anotações separado |
| **Implementação (`src/`, testes)** | Pertence ao **Dia 1 tarde**, fora do escopo desta manhã |
| **`DECISIONS.md`** | Só entradas quando a spec **mudar**; v1.0 inicial não exige log |

---

### Decisões de negócio (para revisão sua)

Vale reler na spec antes da tarde:

1. **Limite diário** — saldo compartilhado por data, consumido na **ordem do array** (d-001/d-002).
2. **NF** — obrigatória só se **valor > 100** (d-003 vs d-004).
3. **Em viagem** — inferido pelo intervalo de **hospedagem** (regex de diárias na descrição); sábado/plantão (d-012) **não** amplia limite sozinho.
4. **Duplicata** — mesma data, categoria, fornecedor, valor e descrição; mantém a primeira (d-007 recusada).
5. **Estorno** — R$ 0 reembolsável, mas **devolve margem** ao limite diário do dia (d-009).

Se quiser outra interpretação em algum AMB, ajustamos a spec + `DECISIONS.md` **antes** de codar.

---

### Commits criados

```
50f0bc8 docs(sessions): export sessao 02 dia 1 manha documentacao
7518556 docs(tasks): fatiar T-001 a T-018 com matriz de cobertura RN/AMB
a8361c1 docs(plan): stack Python, arquitetura em camadas e estrategia de testes
29b9049 docs(spec): spec v1.0 com 12 ambiguidades e regras RN-001 a RN-012
```

**Meta da manhã:** spec/plan/tasks fechados — concluída. Próximo passo: **Dia 1 tarde**, começando por **T-001**. Quer que eu siga com a implementação?

