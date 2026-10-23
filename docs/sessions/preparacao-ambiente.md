# Desafio repository analysis checklist
_Exported on 10/23/2026 at 20:39:21 GMT-3 from Cursor (3.15.6)_

---

**User**

Esse repositório é referente a um desafio que preciso fazer.

Analise o repositório e baseado nos arquivos README.md, DESAFIO.md, RUBRICA.md e FAQ.md faça uma análise do que precisamos executar para cumprir as regras do desafio. Em seguida crie um checklist dos passos que precisamos executar para chegar no resultado esperado

---

**Cursor**

Analisando o repositório e os documentos do desafio.




# Análise do desafio SDD

## O que o desafio realmente mede

O foco não é “código que roda”, e sim **processo Spec-Driven Development**. A pontuação deixa isso explícito:

| Critério | Pontos |
|----------|--------|
| Qualidade da spec (ambiguidades resolvidas, testável, sem vazamento técnico) | **25** |
| Rastreabilidade spec → tasks → commits → testes | **25** |
| Resposta à mudança do Dia 2 (~10h) | **20** |
| Relatório + discernimento (evidências + erro concreto do agente) | **20** |
| Produto funciona (CLI + testes) | **10** |

Um motor perfeito com spec fraca e histórico opaco tende a tirar nota baixa; spec forte, trilha limpa e bug conhecido tendem a ir bem.

## O produto (fixo vs. seu)

**Fixo**

- CLI: `<comando> calcular --input despesas.json --output resultado.json`
- Entrada: formato de [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.json)
- Stack livre; **testes automatizados obrigatórios**

**Seu trabalho de especificação**

- Política do RH (9 itens) com **pelo menos 8 ambiguidades reais**
- Para cada uma: registrar, decidir, justificar em **uma linha**, refletir em regras (`RN-xxx`) na `spec.md`
- **Schema de saída** definido e documentado na spec (não há gabarito único de saída — a correção usa **sua** spec)

**Tipos de ambiguidade (RUBRICA, sem listar as oito)**

- *Unidade de aplicação* (ex.: limite “por dia” — soma de várias despesas no mesmo dia?)
- *Fronteira* (ex.: R$ 100,00 exato e nota fiscal; arredondamento; parcial vs. recusa total)
- *Dado ausente* (ex.: “em viagem” +50% sem campo na entrada)

Cada linha do JSON de exemplo foi pensada para forçar decisões — vale percorrer d-001…d-014 **antes** de fechar a spec.

## Três regras do jogo (obrigatórias)

1. **Nenhum commit sem task** — `feat(T-003): …`, `test(T-003): …`, `docs(spec): …`
2. **Regra só no chat = bug de spec** — atualizar spec + `DECISIONS.md` antes de codar
3. **`/export` ao fim de cada sessão** → `docs/sessions/NN-descricao.md` commitado (sem isso, relatório pode zerar)

## Estado atual do seu repositório

Já existe o commit `chore: estrutura inicial a partir do template`, com `CLAUDE.md`, `specs/`, `docs/RELATORIO.md` ainda no esqueleto. Ainda **não há** `src/`, `tests/`, `docs/sessions/`, e `spec.md` / `plan.md` / `tasks.md` continuam com placeholders.

---

# Checklist executável

### Pré-requisitos (antes / início Dia 1)

- [ ] Fork **público** do repositório (correção precisa do link)
- [ ] Testar `/export` no Claude Code; criar `docs/sessions/` e commitar o primeiro export (`01-…md`)
- [ ] Ler [`exemplos/despesas-exemplo.json`](exemplos/despesas-exemplo.json) item a item anotando “o que a política não diz”
- [ ] Completar [`CLAUDE.md`](CLAUDE.md): linguagem, comandos run/test/lint, convenção monetária

---

### Dia 1 — manhã (documentação antes de código)

- [ ] **`spec.md`**
  - [ ] Problema, objetivo, **fora de escopo** explícito
  - [ ] Entrada (campos) + **saída** (schema + exemplo JSON pequeno)
  - [ ] Regras `RN-001…` desambiguadas, ligadas à política
  - [ ] Seção **≥ 8 ambiguidades** (`AMB-001…`): citação RH, leituras possíveis, decisão, justificativa, RN afetada
  - [ ] Casos de borda alinhados ao JSON (duplicata, competência, estorno, categoria fora da política, hospedagem agregada, etc.)
  - [ ] Critérios de aceite **verificáveis sem código**; zero biblioteca/classe/pasta na spec
  - [ ] Commit: `docs(spec): …`

- [ ] **`plan.md`**
  - [ ] Stack e motivo; arquitetura em blocos; modelo de dados; alternativas descartadas
  - [ ] Estratégia de testes (por RN / por ambiguidade)
  - [ ] Commit: `docs(plan): …`

- [ ] **`tasks.md`**
  - [ ] T-001… fatiadas (1 task ≈ 1 commit); cada uma com **Atende:** (RN/AMB) e **Aceite:** (“teste X passa”)
  - [ ] Matriz de cobertura spec ↔ tasks ↔ testes (no fim do arquivo)
  - [ ] Commit: `docs(tasks): …`

- [ ] Export da sessão → `docs/sessions/02-…md` + commit

---

### Dia 1 — tarde (implementação guiada por tasks)

- [ ] Estrutura `src/` + `tests/` conforme `plan.md`
- [ ] Por task, na ordem:
  - [ ] Ler task em `tasks.md`
  - [ ] Teste que falha → implementação mínima → teste verde
  - [ ] Commit `feat(T-xxx): …` e/ou `test(T-xxx): …`
  - [ ] Marcar `[x]` na task (com hash do commit, se quiser)
- [ ] CLI `calcular --input --output` lendo/escrevendo JSON
- [ ] README **do seu projeto** (substituir o README do desafio): instalar, rodar, testar, exemplo com `despesas-exemplo.json`
- [ ] Rodar suite inteira; processar o JSON de exemplo e conferir saída **contra a spec**
- [ ] Export sessão → `docs/sessions/03-…md` + commit

**Meta Dia 1:** sistema base **funcionando e testado** (libera o Dia 2).

---

### Dia 2 — ~10h (envelope — 20 pts)

- [ ] Ler mudança no canal da turma
- [ ] **Ordem obrigatória:** `spec.md` → entrada em [`DECISIONS.md`](specs/001-motor-reembolso/DECISIONS.md) (o que mudou, por quê, o que quebrou, tasks afetadas) → novas tasks (Fase 5 em `tasks.md`) → código → testes
- [ ] Testes antigos passando ou quebra **justificada** na spec/DECISIONS
- [ ] Commits rastreáveis (`docs(spec):`, `feat(T-0xx):`, etc.)
- [ ] Export sessão do envelope

*(Não precisa estar 100% implementado; penaliza mudança “só no código”.)*

---

### Dia 2 — tarde (fechamento)

- [ ] **`docs/RELATORIO.md`** com evidências (não narrativa vazia):
  - [ ] **Delegação** — tabela o que você vs. Claude; subagentes/skills se usou
  - [ ] **Descrição** — um requisito ambíguo: versão inicial vs. final na spec (ou histórico git)
  - [ ] **Discernimento** — **um erro concreto do agente**: proposta, por que errado, como detectou, o que fez, **link/trecho em `docs/sessions/`** (sem isso, −8 neste critério)
  - [ ] **Diligência** — o que verificou antes de aceitar entregas; autocrítica honesta
  - [ ] **Envelope** — arquivos tocados, tempo, o que a spec facilitou/atrapalhou
- [ ] Último `/export` + commit
- [ ] Revisar penalidades: `DECISIONS.md` se spec mudou; README executável; commits não “wip/final” únicos
- [ ] **Entrega:** link do fork no formulário até **Dia 2, 18h**

---

### Checklist de qualidade (autoavaliação contra RUBRICA)

**Spec (25)**

- [ ] ≥ 8 AMB com decisão + justificativa
- [ ] Nenhuma ambiguidade “resolvida só no código”
- [ ] Escopo negativo claro
- [ ] Aceites testáveis

**Rastreabilidade (25)**

- [ ] Todo commit referencia task ou `docs(spec|plan|tasks)`
- [ ] Toda RN testável tem teste nomeado de forma reconhecível
- [ ] Ordem temporal plausível: spec/plan/tasks → depois código
- [ ] Tasks marcadas ao longo do tempo, não tudo de uma vez

**Relatório (20)**

- [ ] Sessões exportadas em **várias** datas/sessões (não um dump no último minuto)
- [ ] Discernimento verificável com citação de sessão

**Produto (10)**

- [ ] README permite rodar sem adivinhação
- [ ] Testes passando
- [ ] Comportamento = o que **sua** spec diz (inclusive casos “estranhos” do exemplo)

---

## Mapa mental: o JSON de exemplo vs. o trabalho

Use isto como roteiro de leitura da spec (não substitui as 8+ ambiguidades da política):

| Item | Gatilho típico |
|------|----------------|
| d-001 + d-002 | Limite diário de alimentação (agregação por data) |
| d-003 vs d-004 | Limiar R$ 100 e nota fiscal (fronteira) |
| d-005 | Categoria fora da política |
| d-006 + d-007 | Duplicatas |
| d-008 | Competência do período |
| d-009 | Valor negativo / estorno |
| d-010, d-013 | Hospedagem (diária vs. lançamento único; NF) |
| d-011 | Precisão decimal / arredondamento |
| d-012 | Despesa em fim de semana (se relevante à sua spec) |
| d-014 | Normalização de categoria (`ALIMENTACAO`) |
| (política item 6) | “Em viagem” +50% **sem campo na entrada** |

---

## Prioridade se o tempo apertar

1. Spec completa (8+ AMB) + `DECISIONS.md` disciplinado  
2. Rastreabilidade (tasks + commits + testes por regra)  
3. Envelope pelo fluxo spec-first  
4. Relatório com discernimento **concreto** + sessões exportadas  
5. Produto — só depois disso vale otimizar “100% dos casos ocultos”

Se quiser, no próximo passo podemos começar pelo **Dia 1 manhã**: percorrer o JSON juntos e esboçar a lista de `AMB-xxx` antes de preencher a `spec.md` (sem implementar ainda).

---

**User**

Crie um arquivo CHECKLIST.md na raiz do projeto com as informações desse checklist que você criou. Após isso adicione ao gitignore esse arquivo para que não entre nos commits

---

**Cursor**

Feito.

1. **`CHECKLIST.md`** na raiz — checklist completo (pontuação, regras do jogo, Dia 1/2, autoavaliação, tabela do JSON de exemplo e prioridades).

2. **`.gitignore`** — entrada `CHECKLIST.md` na seção de arquivos locais.

O Git confirma que `CHECKLIST.md` está ignorado; só `.gitignore` aparece como modificado. Se quiser versionar a regra de ignore no fork (sem incluir o checklist), faça um commit só do `.gitignore`, por exemplo: `chore: ignorar CHECKLIST.md local`.

