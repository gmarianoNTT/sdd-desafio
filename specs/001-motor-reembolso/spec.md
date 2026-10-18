# Spec — Motor de Cálculo de Reembolso

**Versão:** 1.0 · **Status:** aprovada para implementação · **Última alteração:** 2026-10-18

> **Regra de ouro deste arquivo:** ele descreve o QUÊ e o PORQUÊ. Nenhuma linha
> aqui pode citar linguagem, biblioteca, classe, função ou estrutura de pasta.
> Se apareceu solução, o lugar dela é o `plan.md`.
>
> **Teste de aceitação da própria spec:** uma pessoa que nunca viu o projeto
> consegue, lendo só este arquivo, verificar se o sistema está correto?

---

## 1. Problema

O financeiro reembolsa despesas de colaboradores conferindo manualmente cada
lançamento contra a política do RH. O processo é lento, sujeito a interpretações
diferentes entre analistas e gera retrabalho quando a justificativa de uma recusa
não está clara.

## 2. Objetivo

Dado um JSON com as despesas de um colaborador em um período de competência, o
sistema produz, para **cada despesa**, o valor reembolsável e uma justificativa
auditável, aplicando a política de forma consistente.

## 3. Fora de escopo

- Não faz interface web, API HTTP ou autenticação.
- Não persiste histórico, não integra com ERP nem gera ordem de pagamento.
- Não valida veracidade de notas fiscais nem consulta Receita Federal.
- Não corrige ou rejeita o JSON de entrada por campos ausentes além do que esta
  spec define — assume entrada bem formada no formato do exemplo.
- Não infere “em viagem” a partir de calendário de fim de semana, plantão ou
  descrição textual genérica — apenas pela regra de hospedagem descrita em RN-006.
- Não reembolsa categorias que não constam explicitamente na política (itens 1–3
  e 9), salvo normalização de grafia (AMB-010).

## 4. Entrada e saída

### Entrada

Conforme `exemplos/despesas-exemplo.json`.

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | texto | Identificador do colaborador | sim |
| `colaborador.nome` | texto | Nome (informativo) | sim |
| `colaborador.centro_custo` | texto | Centro de custo (informativo) | sim |
| `periodo.competencia` | texto | Competência `AAAA-MM` | sim |
| `periodo.inicio` | data `AAAA-MM-DD` | Primeiro dia do período válido | sim |
| `periodo.fim` | data `AAAA-MM-DD` | Último dia do período válido | sim |
| `despesas[].id` | texto | Identificador único da despesa | sim |
| `despesas[].data` | data | Data do lançamento | sim |
| `despesas[].categoria` | texto | Tipo de despesa | sim |
| `despesas[].descricao` | texto | Descrição livre | sim |
| `despesas[].fornecedor` | texto | Fornecedor | sim |
| `despesas[].valor` | número | Valor em reais (pode ser negativo) | sim |
| `despesas[].tem_nota_fiscal` | booleano | Indica se há NF | sim |

A ordem do array `despesas` é **significativa** para duplicatas e para consumo
de limite diário (RN-004, RN-008).

### Saída

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador.id` | texto | Eco do identificador de entrada |
| `periodo.competencia` | texto | Eco da competência de entrada |
| `itens[].id` | texto | Id da despesa correspondente |
| `itens[].valor_informado` | número | Valor da entrada (2 casas decimais) |
| `itens[].valor_reembolsavel` | número | Valor aprovado para reembolso (≥ 0) |
| `itens[].status` | texto | `aprovado`, `parcial` ou `recusado` |
| `itens[].justificativa` | texto | Explicação legível da decisão |
| `resumo.total_informado` | número | Soma dos `valor_informado` |
| `resumo.total_reembolsavel` | número | Soma dos `valor_reembolsavel` |

**Status:**

- `aprovado` — `valor_reembolsavel` = valor elegível após regras (pode ser menor
  que `valor_informado` só quando parcial por limite; se igual ao elegível cheio,
  aprovado).
- `parcial` — despesa elegível em parte; `0 < valor_reembolsavel < valor_informado`
  (limite diário ou limite por diária de hospedagem).
- `recusado` — `valor_reembolsavel` = 0.

**Exemplo** (entrada mínima fictícia):

Entrada:

```json
{
  "colaborador": { "id": "c-1", "nome": "Ana", "centro_custo": "CC-1" },
  "periodo": { "competencia": "2026-07", "inicio": "2026-07-01", "fim": "2026-07-31" },
  "despesas": [
    {
      "id": "x-1",
      "data": "2026-07-03",
      "categoria": "alimentacao",
      "descricao": "Almoco",
      "fornecedor": "Bar",
      "valor": 72.5,
      "tem_nota_fiscal": true
    }
  ]
}
```

Saída:

```json
{
  "colaborador": { "id": "c-1" },
  "periodo": { "competencia": "2026-07" },
  "itens": [
    {
      "id": "x-1",
      "valor_informado": 72.5,
      "valor_reembolsavel": 60.0,
      "status": "parcial",
      "justificativa": "Limite diário de alimentação (R$ 60,00); reembolso parcial do excedente."
    }
  ],
  "resumo": {
    "total_informado": 72.5,
    "total_reembolsavel": 60.0
  }
}
```

---

## 5. Regras de negócio

Categorias cobertas pela política: **alimentação**, **transporte urbano**,
**hospedagem** (após normalização AMB-010).

### RN-001 — Limite diário de alimentação

**Regra:** Por **data civil** (`despesas[].data`), a soma dos valores
reembolsáveis de despesas de alimentação naquele dia não pode exceder **R$ 60,00**,
salvo RN-006 (em viagem).
**Origem:** política do RH, item 1.
**Aceite:** Para `2026-07-03`, despesas d-001 (R$ 72,50) e d-002 (R$ 38,00): após
processamento em ordem de entrada, d-001 recebe R$ 60,00 parcial e d-002 R$ 0,00
recusado por esgotamento do limite diário.

### RN-002 — Limite diário de transporte urbano

**Regra:** Por data civil, a soma dos valores reembolsáveis de transporte urbano
não pode exceder **R$ 80,00** por dia, salvo RN-006.
**Origem:** política do RH, item 2.
**Aceite:** Três corridas de R$ 30 no mesmo dia resultam em R$ 80 reembolsáveis
no total (parcial na terceira se necessário), na ordem do array.

### RN-003 — Limite de hospedagem por diária

**Regra:** Cada **diária** inferida de uma despesa de hospedagem tem teto de
**R$ 250,00** de valor reembolsável; valor da despesa é rateado pelo número de
diárias (AMB-008). O reembolso da linha é a soma do reembolso de cada diária,
limitado ao `valor` informado.
**Origem:** política do RH, item 3.
**Aceite:** d-010 (R$ 480, 2 diárias) → R$ 240/diária → reembolso integral R$ 480.
d-013 (R$ 690, 3 noites, sem NF) → tratado em RN-005 antes do limite de hospedagem.

### RN-004 — Reembolso parcial acima do limite

**Regra:** Quando uma regra de teto (diário ou por diária) se aplica, **não** se
recusa o item inteiro por excesso: paga-se até o teto disponível e o excedente
não é reembolsado (AMB-002).
**Origem:** política do RH, item 4.
**Aceite:** d-001 recebe R$ 60,00 de R$ 72,50 com status `parcial`, não R$ 0.

### RN-005 — Nota fiscal acima de R$ 100

**Regra:** Se `valor` **estritamente maior** que R$ 100,00 e `tem_nota_fiscal`
for falso, a despesa inteira é **não reembolsável** (R$ 0).
**Origem:** política do RH, item 5.
**Aceite:** d-003 (R$ 100,00, sem NF) pode ser reembolsada se passar demais
regras; d-004 (R$ 100,01, sem NF) → R$ 0.

### RN-006 — Colaborador em viagem (+50% nos limites)

**Regra:** Nas datas em que o colaborador está **em viagem** (definição AMB-004),
os tetos de RN-001, RN-002 e RN-003 aumentam 50% (alimentação R$ 90, transporte
R$ 120, hospedagem R$ 375 por diária).
**Origem:** política do RH, item 6.
**Aceite:** Despesa de alimentação em data coberta por hospedagem inferida usa
teto R$ 90,00/dia.

### RN-007 — Competência do período

**Regra:** Despesa com `data` **fora** do intervalo [`periodo.inicio`, `periodo.fim`]
(inclusivo) → `valor_reembolsavel` = 0, status `recusado`.
**Origem:** política do RH, item 7.
**Aceite:** d-008 (`2026-04-15` com período julho) → R$ 0.

### RN-008 — Duplicatas

**Regra:** Duplicatas (AMB-005) após a primeira ocorrência na ordem do array
recebem R$ 0 e não consomem limite diário.
**Origem:** política do RH, item 8.
**Aceite:** d-006 mantém reembolso; d-007 → R$ 0 como duplicata.

### RN-009 — Categoria fora da política

**Regra:** Categorias distintas de alimentação, transporte urbano e hospedagem
(após normalização) → R$ 0.
**Origem:** política do RH, item 9.
**Aceite:** d-005 (`coworking`) → R$ 0.

### RN-010 — Estorno (valor negativo)

**Regra:** Despesa com `valor` < 0 não gera reembolso positivo; `valor_reembolsavel`
= 0. O valor negativo **devolve margem** ao limite diário da categoria na mesma
data, considerando ordem do array (AMB-007).
**Origem:** política do RH (silêncio) + item d-009 do exemplo.
**Aceite:** d-009 → R$ 0; uma corrida posterior no mesmo dia pode reembolsar até
R$ 80 considerando o estorno anterior na ordem do arquivo.

### RN-011 — Arredondamento monetário

**Regra:** Valores na saída usam **duas casas decimais**, arredondamento
half-away-from-zero (AMB-011).
**Origem:** exemplo d-011.
**Aceite:** Valor reembolsável derivado de R$ 33,333 aparece como R$ 33,33 na saída.

### RN-012 — Consumo de limite diário na ordem de entrada

**Regra:** Para RN-001 e RN-002, o limite diário é um **saldo compartilhado** por
(data, categoria). Cada despesa elegível consome `min(valor, saldo_restante)` na
ordem em que aparece em `despesas`.
**Origem:** AMB-001, AMB-002.
**Aceite:** Par d-001/d-002 conforme RN-001.

---

## 6. Ambiguidades identificadas e decisões

### AMB-001 — “R$ 60 por dia” — unidade do limite

**Texto original do RH:** "Alimentação tem limite de **R$ 60 por dia**."
**O que não está claro:** Limite por despesa individual ou soma de todas as
refeições na mesma data?
**Decisão:** Teto **agregado por data civil** e categoria (RN-001, RN-012).
**Justificativa:** “Por dia” no contexto de prestação de contas refere-se ao dia
calendário, não a cada lançamento isolado.
**Regra afetada:** RN-001, RN-002, RN-012

### AMB-002 — “Reembolsadas parcialmente”

**Texto original do RH:** "Despesas **acima do limite** são reembolsadas parcialmente."
**O que não está claro:** Pagar até o limite e cortar só o excedente, ou recusar
o lançamento inteiro?
**Decisão:** Reembolsar até o teto disponível; excedente não pago (RN-004).
**Justificativa:** “Parcialmente” implica pagamento parcial, não recusa total.
**Regra afetada:** RN-004

### AMB-003 — Fronteira “acima de R$ 100” e nota fiscal

**Texto original do RH:** "**Nota fiscal é obrigatória acima de R$ 100.**"
**O que não está claro:** R$ 100,00 exatos exigem NF?
**Decisão:** Obrigatória apenas se `valor > 100,00` (RN-005).
**Justificativa:** “Acima de” em normas corporativas costuma ser estrito; evita
penalizar o limiar exato (d-003 vs d-004).
**Regra afetada:** RN-005

### AMB-004 — “Em viagem” sem campo na entrada

**Texto original do RH:** "Colaborador **em viagem** tem limites ampliados em 50%."
**O que não está claro:** Como detectar viagem sem atributo no JSON?
**Decisão:** Uma data está “em viagem” se cai no intervalo de permanência inferido
de alguma despesa de **hospedagem** no mesmo arquivo: `data` da hospedagem = primeiro
dia; número de diárias = inteiro extraído de `descricao` (`N diaria(s)`, `N noite(s)`,
case insensitive); se ausente, **1** diária; dias cobertos = `data` até
`data + (N - 1)` inclusive.
**Justificativa:** Hospedagem é o único indicador objetivo disponível na entrada;
fim de semana ou “plantão” (d-012) não ampliam limite sozinhos.
**Regra afetada:** RN-006

### AMB-005 — “Duplicatas devem ser tratadas”

**Texto original do RH:** "**Duplicatas devem ser tratadas.**"
**O que não está claro:** Mesclar, somar, recusar todas, recusar repetidas?
**Decisão:** Duplicata = mesma `data`, mesma categoria normalizada, mesmo
`fornecedor`, mesmo `valor` e mesma `descricao` (comparação case-insensitive,
espaços normalizados). Mantém-se a **primeira** na ordem do array; demais → R$ 0
(RN-008).
**Justificativa:** Preserva um lançamento legítimo e bloqueia reenvio acidental
(d-006/d-007).
**Regra afetada:** RN-008

### AMB-006 — Competência vs data da despesa

**Texto original do RH:** "Despesas devem ser lançadas **dentro do período de competência**."
**O que não está claro:** Usar só `competencia` textual ou o intervalo `inicio`/`fim`?
**Decisão:** Validar `despesas[].data` contra `periodo.inicio` e `periodo.fim` (RN-007).
**Justificativa:** O JSON já traz intervalo explícito; evita ambiguidade de mês
vs competência contábil.
**Regra afetada:** RN-007

### AMB-007 — Valor negativo / estorno

**Texto original do RH:** *(silêncio — item d-009 no exemplo)*
**O que não está claro:** Estorno reduz limite, gera crédito ou é ignorado?
**Decisão:** RN-010 — reembolso zero; valor negativo aumenta saldo disponível
do limite diário da categoria na mesma data, na ordem do array.
**Justificativa:** Estorno reflete cancelamento de gasto anterior; devolver margem
evita punir o mesmo dia.
**Regra afetada:** RN-010

### AMB-008 — Hospedagem em lançamento único (várias diárias)

**Texto original do RH:** "Hospedagem tem limite de **R$ 250 por diária**."
**O que não está claro:** Uma fatura única de várias noites — limite sobre total ou por noite?
**Decisão:** Inferir N diárias pela descrição; calcular `valor_por_diaria = valor / N`;
reembolso por diária = `min(valor_por_diaria, teto_diaria)`; somar N diárias,
limitado a `valor` (RN-003).
**Justificativa:** Política fala em “por diária”; rateio é a leitura coerente
(d-010, d-013).
**Regra afetada:** RN-003

### AMB-009 — Categoria ausente na política

**Texto original do RH:** "**Categorias fora da política não são reembolsáveis.**"
**O que não está claro:** Coworking, material, etc.
**Decisão:** Apenas as três categorias da política reembolsam; demais → R$ 0 (RN-009).
**Justificativa:** Lista fechada implícita nos itens 1–3 e 9.
**Regra afetada:** RN-009

### AMB-010 — Normalização de categoria

**Texto original do RH:** *(silêncio — d-014 `ALIMENTACAO`)*
**O que não está claro:** Maiúsculas, acentos, espaços?
**Decisão:** Normalizar para minúsculas sem acento, trim; `ALIMENTACAO` → alimentacao.
**Justificativa:** Evita recusa por formato; categoria semântica é a mesma.
**Regra afetada:** RN-001, RN-009

### AMB-011 — Precisão decimal

**Texto original do RH:** *(silêncio — d-011 valor 33,333)*
**O que não está claro:** Quantas casas na saída e como arredondar?
**Decisão:** RN-011 — duas casas decimais na saída, half-away-from-zero.
**Justificativa:** Padrão monetário BRL em relatórios corporativos.
**Regra afetada:** RN-011

### AMB-012 — Fim de semana e plantão

**Texto original do RH:** *(silêncio — d-012 sábado)*
**O que não está claro:** Limite diferente em fim de semana?
**Decisão:** Mesmas regras que dias úteis; sem acréscimo automático por ser sábado/domingo.
**Justificativa:** Política não distingue; ampliar só por RN-006 quando em viagem.
**Regra afetada:** RN-001 (sem alteração de teto)

---

## 7. Casos de borda

| Caso | Entrada (ref.) | Comportamento esperado | Regra |
|---|---|---|---|
| Duas refeições no mesmo dia | d-001, d-002 | Soma cap R$ 60/dia; parcial + recusa por saldo | RN-001, RN-012 |
| NF no limiar | d-003 vs d-004 | 100,00 OK sem NF; 100,01 exige NF | RN-005, AMB-003 |
| Categoria proibida | d-005 | R$ 0 | RN-009 |
| Duplicata | d-006, d-007 | Primeira OK; segunda R$ 0 | RN-008 |
| Fora da competência | d-008 | R$ 0 | RN-007 |
| Estorno | d-009 | R$ 0; devolve margem diária transporte | RN-010 |
| Hospedagem multi-noite | d-010 | Rateio 480/2; teto por diária | RN-003, AMB-008 |
| Valor com 3 decimais | d-011 | Saída arredondada 2 casas | RN-011 |
| Sábado sem viagem | d-012 | Limite normal R$ 60/dia alimentação | AMB-012 |
| Hospedagem sem NF > 100 | d-013 | R$ 0 por RN-005 antes de rateio | RN-005 |
| Categoria maiúscula | d-014 | Tratada como alimentação | AMB-010 |

---

## 8. Ordem de aplicação das regras

Para cada despesa, **na ordem do array** `despesas`:

1. **Normalizar** categoria (AMB-010).
2. **Duplicata** — se repetida, resultado R$ 0 e pular demais etapas (RN-008).
3. **Competência** — fora do intervalo → R$ 0 (RN-007).
4. **Categoria** — se fora da política → R$ 0 (RN-009).
5. **Nota fiscal** — se `valor > 100` sem NF → R$ 0 (RN-005).
6. **Estorno** — se `valor < 0` → R$ 0 e ajustar saldo diário (RN-010); encerrar.
7. **Hospedagem** — calcular reembolso por diárias e teto RN-003 (com RN-006 se em viagem).
8. **Demais categorias** — aplicar teto diário RN-001/RN-002 com saldo compartilhado (RN-012) e RN-006.
9. **Arredondar** `valor_reembolsavel` (RN-011) e definir `status`/`justificativa`.

**Pré-processamento:** antes do passo 7–8, calcular conjunto de datas “em viagem”
a partir de todas as despesas de hospedagem (AMB-004).

Duplicatas e competência precedem consumo de limite para não distorcer saldo.
Nota fiscal precede rateio de hospedagem para d-013.

---

## 9. Critérios de aceite

O sistema está pronto quando:

- [ ] A CLI aceita `--input` e `--output`, lê o JSON de entrada e grava saída conforme schema desta seção 4.
- [ ] Cada item d-001 … d-014 do arquivo `exemplos/despesas-exemplo.json` produz `valor_reembolsavel` e `status` coerentes com as regras RN-001 … RN-012 e decisões AMB-001 … AMB-012.
- [ ] Nenhuma despesa duplicada (d-007) recebe reembolso; d-006 sim.
- [ ] d-008 recusada; d-005 recusada; d-004 recusada por NF; d-003 elegível se dentro de demais regras.
- [ ] Soma em `resumo.total_reembolsavel` igual à soma dos itens na saída.
- [ ] Suite de testes automatizados cobre cada RN listada e referencia IDs RN/AMB nos nomes ou documentação dos casos.

---

## 10. O que fica em aberto

- **Centro de custo / aprovação gerencial:** campos existem na entrada mas não
  alteram cálculo — decisão provisória: ignorar até nova spec.
- **Envelope Dia 2:** mudanças de requisito serão registradas em `DECISIONS.md`
  quando publicadas.
