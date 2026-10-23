# Relatório — Desafio SDD

**Aluno:** *(preencher nome no formulário)* · **Repositório:** https://github.com/gmarianoNTT/sdd-desafio · **Data:** 2026-10-23

> Evidências cruzadas com `docs/sessions/`, hashes de commit e arquivos da spec.

---

## Delegação

**A divisão:**

| Atividade | Quem | Por quê |
|---|---|---|
| Identificar ambiguidades | Eu + agente (Cursor) | Percorri `exemplos/despesas-exemplo.json` e a política RH; o agente redigiu rascunhos de AMB na sessão 02 (`29b9049`). |
| Decidir as ambiguidades | Eu | Cada AMB exige escolha de produto; conferi casos d-001…d-014 antes de marcar aceite na spec. |
| Escrever a spec / plan / tasks | Agente, revisão minha | Dia 1 manhã: commits `docs(spec|plan|tasks):` (`29b9049`, `a8361c1`, `7518556`). |
| Desenhar a arquitetura | Agente + `plan.md` | Núcleo `motor/` sem I/O; política na borda após envelope (`plan.md` v1.1, `01fd542`). |
| Implementar | Agente (Cursor) | T-001…T-026 guiados por `tasks.md`; eu disparei por checklist e corrigi desvios (ex. DECISIONS). |
| Escrever testes | Agente | Nomes `test_RN_*` / `test_AMB_*` / envelope; eu rodei `python -m pytest` antes de aceitar entregas. |
| Absorver o envelope | Eu (ordem) + agente (execução) | Impus fluxo spec → DECISIONS → tasks → código (`04-dia2-envelope-v4.md`); agente implementou T-019…T-026. |

**Onde deleguei e me arrependi:**

- Deixei o agente commitar spec v2 e motor v4 em paralelo: surgiu o commit `f23119c` só com “Co-authored-by…”, sem mensagem `docs(spec):` útil — corrigi depois com `50c821f` / `b614847`, mas o histórico ficou ruidoso.

**Onde não deleguei e deveria ter delegado:**

- Renomear/rebase de commits problemáticos — adiei; a rastreabilidade ainda é legível via `tasks.md` e mensagens seguintes.

**Subagentes / skills / MCP / hooks:** Não usei subagentes nem MCP neste fork. Trabalho em sessões Cursor com export manual para `docs/sessions/*.md` (equivalente ao `/export` do desafio). Skills padrão do Cursor (regras em `CLAUDE.md`) bastaram.

---

## Descrição

*Requisito ambíguo: centro de custo na entrada.*

**Versão 1 (spec v1.0, commit base Dia 1):**

> `colaborador.centro_custo` — Centro de custo **(informativo)**  
> §10: “campos existem na entrada mas **não alteram cálculo** — decisão provisória: **ignorar** até nova spec.”

*(Trecho de `spec.md` em `d0ed763`.)*

**Versão final (spec v2.0+, RN-015):**

> `colaborador.centro_custo` — Centro de custo — **seleciona limites (RN-015)**  
> RN-015: mapa efetivo = `padrao` + override por CC; CC ausente usa **apenas** `padrao` (AMB-013).

*( `specs/001-motor-reembolso/spec.md` §4 e RN-015; registrado em D-001.)*

**O que estava ambíguo:** A política RH menciona centros de custo, mas o JSON de exemplo traz `CC-ENG-PLATAFORMA` sem efeito na v1 — era provisório ou requisito futuro?

**Como percebi:** O envelope v4 (`exemplos/envelope/00-ENVELOPE-LACRADO.md`) tornou o CC **obrigatório** para limites; `f-003` (`representacao` em CC desconhecido) não fecha sem RN-015/AMB-013.

**Commit da mudança:** `b614847` (`docs(spec): D-001 envelope v4…`) + implementação `6bec477` / `56e0451`.

---

## Discernimento

### Caso 1 — Numeração errada em `DECISIONS.md`

**O que ele propôs:** Registrar a absorção do envelope v4 como entrada **D-002**, mantendo um placeholder antigo como D-001 (`04-dia2-envelope-v4.md`, resumo da primeira leva Dia 2).

**Por que estava errado:** O desafio pede log cronológico claro; a mudança estrutural v1→v2 **é** a primeira decisão pós-envelope e deve ser **D-001**. Item C (fila manual) vem depois como **D-002**.

**Como eu detectei:** Li `DECISIONS.md` após a entrega e comparei com a ordem do envelope (A/B antes de C) — prompt explícito na sessão 04.

**O que eu fiz:** Pedi renumerar; agente corrigiu e implementou RN-016 em seguida (`b614847`).

**Onde está a evidência:** `docs/sessions/04-dia2-envelope-v4.md` — bloco *“Primeiro, atualize… D-002, porém deveria ser a D-001”* e resumo *“DECISIONS.md — D-002 → D-001”*.

### Caso 2 *(opcional)* — Tipo de commit vs. conteúdo

**O que ele propôs:** `test(T-026): …` incluindo alterações em `motor/politica.py` / `calcular.py` (`c87e556`).

**Por que estava errado:** Convenção do desafio separa `feat(T-xxx)` (código) de `test(T-xxx)` (só testes).

**Como eu detectei:** `git show c87e556 --stat` mostra motor + testes no mesmo commit.

**O que eu fiz:** Aceitei para não reescrever histórico; documentei em `tasks.md` e neste relatório. Comportamento coberto por `f467c06` e 23 testes verdes.

**Padrão que notei:** Em entregas grandes (envelope), o agente agrupa arquivos relacionados num commit só; preciso pedir commits atômicos por task explicitamente.

---

## Diligência

**Procedimento de verificação:**

1. Ler a task em `tasks.md` antes de marcar `[x]`.
2. Rodar `python -m pytest` após cada leva (18 → 21 → 23 testes).
3. Executar CLI nos JSON do envelope e no `despesas-exemplo.json` com `--politica` / `--cambio`.
4. Conferir status críticos (e-006 recusa GBP, e-007 `pendente`, f-003 `representacao` recusada).

**Li o diff inteiro em que porcentagem das entregas?** ~40% no Dia 1; ~60% no envelope (foco em `spec.md`, `DECISIONS.md`, `calcular.py` e testes envelope).

**Aceitei sem verificar direito:**

- Mensagem do commit `f23119c` — só percebi ao revisar log para o relatório.
- Não rodei `ruff` de forma sistemática (opcional no `CLAUDE.md`).

**Testes:** Escritos pelo agente; validação cruzada com IDs da spec (d-*, e-*, f-*) e com decisões AMB (ex. AMB-018 NF sobre valor convertido em `test_envelope_v4.py` / e-005). Testes de fronteira RN-016 adicionados em `test_rn_016.py` após eu exigir item C.

---

## O envelope

**Quantos arquivos toquei na mão:** ~15 revisados linha a linha (spec, DECISIONS, README, sessões); o agente alterou **41 arquivos** na leva v4.

**Quanto tempo levou:** ~1 sessão Cursor para análise + arquivos (`63ad031`); ~1 sessão para spec/código/testes; ~½ sessão para item C e fechamento.

**Diff de absorção:** 41 arquivos, +1205 / −457 linhas (`git diff d0ed763..HEAD --stat`, último commit base pré-envelope `d0ed763`).

**Absorveu de graça:**

- Pipeline ordenado (competência → duplicata → NF → limites) — só entrou conversão antes de NF/limites (RN-013).
- Saldo diário compartilhado (RN-012) — passou a usar valores já em BRL (AMB-019).
- Testes por RN — fixtures ganharam `politica`/`cambio` em `conftest.py`.

**Resistiu:**

- `motor/politica.py` com constantes globais — substituído por `politica_config.py` + JSON (`D-001`).
- §10 “ignorar centro_custo” — revogado; regressão em `despesas-exemplo.json` (CC-ENG, d-010 R$ 0).
- Saída só 3 status — RN-016 / `pendente` (D-002).

**Ordem em que fiz:** spec v2 → D-001 → tasks Fase 5 → plan → código (T-019…) → testes → spec v2.1 + D-002 + T-026. Timestamps dos commits respeitam essa ordem (`63ad031` … `beb8d66`).

**Se eu tivesse escrito a spec original sabendo desta mudança:** Teria parametrizado limites desde o Dia 1 (política injetável), evitando hardcode R$ 60/80/250.

**O que a spec me poupou, em concreto:**

- GBP sem cotação (e-006): AMB-017 já decidida → recusa, não inventar “última moeda”.
- CC-SUPORTE-N2 + `representacao` (f-003): AMB-013 → só categorias do `padrao`, teste `test_envelope_cc_desconhecido`.

---

## Fechamento

**Para qual tamanho de projeto isto valeu a pena?** Domínio com dezenas de regras explícitas e mudança de requisito no meio — spec + tasks evitaram retrabalho cego no motor.

**Para qual não valeria?** Spike descartável ou script de uma regra só — o custo de AMB/DECISIONS seria overhead.

**O que eu faria diferente:** Commits atômicos por task desde o T-003 (núcleo ficou grande no Dia 1); rebase do `f23119c` antes de entregar.

**A coisa mais desconfortável que aprendi:** O agente entrega código “verde” rápido; sem ler `DECISIONS.md` e a sessão exportada, eu confundia **ordem documental** com **ordem de negócio** (caso D-001/D-002).
