# Spec — Motor de Cálculo de Reembolso

**Versão:** 2.1 (Política v4 + fila manual) · **Status:** aprovada para implementação · **Última alteração:** 2026-10-23

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

Dado um JSON com as despesas de um colaborador em um período de competência e os
arquivos de **política** e **câmbio** vigentes, o sistema produz, para **cada
despesa**, o valor reembolsável (em moeda base da política, BRL) e uma
justificativa auditável, aplicando a política de forma consistente.

## 3. Fora de escopo

- Não faz interface web, API HTTP ou autenticação.
- Não persiste histórico, não integra com ERP nem gera ordem de pagamento.
- Não valida veracidade de notas fiscais nem consulta Receita Federal.
- Não corrige ou rejeita o JSON de entrada por campos ausentes além do que esta
  spec define — assume entrada bem formada no formato do exemplo.
- Não infere “em viagem” a partir de calendário de fim de semana, plantão ou
  descrição textual genérica — apenas pela regra de hospedagem descrita em RN-006.
- Não reembolsa categorias que não constam no mapa efetivo de limites do centro
  de custo (RN-009), salvo normalização de grafia (AMB-010).
- Não executa aprovação/rejeição pelo gestor — apenas marca itens **pendentes**
  (RN-016); não há workflow de fila persistida.

## 4. Entrada e saída

### Entrada

Lote de despesas conforme `exemplos/despesas-exemplo.json` e exemplos do envelope
(`exemplos/envelope/`). O sistema também recebe, por parâmetro de execução, o
caminho do arquivo de política (formato `politica-v4.json`) e o arquivo de câmbio
(`cambio.json`).

| Campo | Tipo | Significado | Obrigatório |
|---|---|---|---|
| `colaborador.id` | texto | Identificador do colaborador | sim |
| `colaborador.nome` | texto | Nome (informativo) | sim |
| `colaborador.centro_custo` | texto | Centro de custo — seleciona limites (RN-015) | sim |
| `periodo.competencia` | texto | Competência `AAAA-MM` | sim |
| `periodo.inicio` | data `AAAA-MM-DD` | Primeiro dia do período válido | sim |
| `periodo.fim` | data `AAAA-MM-DD` | Último dia do período válido | sim |
| `despesas[].id` | texto | Identificador único da despesa | sim |
| `despesas[].data` | data | Data do lançamento | sim |
| `despesas[].categoria` | texto | Tipo de despesa | sim |
| `despesas[].descricao` | texto | Descrição livre | sim |
| `despesas[].fornecedor` | texto | Fornecedor | sim |
| `despesas[].valor` | número | Valor na moeda informada (pode ser negativo) | sim |
| `despesas[].moeda` | texto ISO 4217 | Moeda do `valor`; se ausente, `BRL` (RN-013) | não |
| `despesas[].tem_nota_fiscal` | booleano | Indica se há NF | sim |

A ordem do array `despesas` é **significativa** para duplicatas e para consumo
de limite diário (RN-004, RN-008, RN-012).

**Política externa (`politica-v4.json`):** contém `padrao` (limites por categoria),
`centros_custo` (overrides parciais ou totais por centro), `nota_fiscal_obrigatoria_acima_de`,
`acrescimo_em_viagem_percentual`, `aprovacao_manual_acima_de` (RN-016; se ausente,
R$ 500,00) e `moeda_base` (BRL). Categorias e tetos vêm somente deste arquivo.

**Câmbio (`cambio.json`):** mapa `taxas[AAAA-MM-DD][MOEDA]` → fator para converter
unidade da moeda estrangeira em BRL (multiplicar `valor` pelo fator).

### Saída

| Campo | Tipo | Significado |
|---|---|---|
| `colaborador.id` | texto | Eco do identificador de entrada |
| `periodo.competencia` | texto | Eco da competência de entrada |
| `itens[].id` | texto | Id da despesa correspondente |
| `itens[].valor_informado` | número | `valor` da entrada (2 casas decimais), na moeda informada |
| `itens[].valor_reembolsavel` | número | Valor calculado em **BRL** (≥ 0); inclui pendentes |
| `itens[].status` | texto | `aprovado`, `parcial`, `recusado` ou `pendente` (RN-016) |
| `itens[].justificativa` | texto | Explicação legível da decisão |
| `resumo.total_informado` | número | Soma dos `valor_informado` (valores brutos da entrada) |
| `resumo.total_reembolsavel` | número | Soma dos `valor_reembolsavel` em BRL |

**Status** (comparação interna usa valor convertido em BRL quando `moeda` ≠ BRL):

- `aprovado` — reembolso integral do valor elegível após regras.
- `parcial` — `0 < valor_reembolsavel <` valor elegível em BRL antes de cortes
  por teto diário/diária, ou corte por limite agregado.
- `recusado` — `valor_reembolsavel` = 0.
- `pendente` — `valor_reembolsavel` > 0 e **estritamente maior** que
  `aprovacao_manual_acima_de` da política; cálculo de limites/NF concluído, mas
  reembolso automático bloqueado — aguarda gestor (RN-016). Substitui o status
  `aprovado` ou `parcial` que seria atribuído antes da fila.

---

## 5. Regras de negócio

Categorias reembolsáveis são **as que possuem entrada** no mapa efetivo de limites
do centro de custo (RN-015), após normalização (AMB-010). Exemplos típicos:
alimentação, transporte urbano, hospedagem, representação (quando prevista na política).

### RN-001 — Limite diário de alimentação

**Regra:** Por **data civil**, a soma dos valores reembolsáveis (BRL) de
alimentação naquele dia não pode exceder o teto **efetivo** de alimentação do
centro de custo (`periodicidade` = dia), salvo RN-006.
**Origem:** política v4 / item alimentação.
**Aceite:** Centro com teto padrão R$ 60: par d-001/d-002 em `2026-07-03` → d-001
R$ 60 parcial e d-002 R$ 0. Centro `CC-ENG-PLATAFORMA` (teto R$ 75): d-001 R$ 72,50
aprovado; d-002 R$ 2,50 parcial.

### RN-002 — Limite diário de transporte urbano

**Regra:** Por data civil, soma dos reembolsos de transporte urbano em BRL não
excede o teto efetivo (`periodicidade` = dia), salvo RN-006.
**Origem:** política v4.
**Aceite:** Três corridas de R$ 30 no mesmo dia (CC com teto R$ 80) → R$ 80 total.

### RN-003 — Limite de hospedagem por diária

**Regra:** Cada diária inferida (AMB-008) tem teto efetivo de reembolso em BRL
(`periodicidade` = diária); rateio do `valor` convertido em BRL. Teto **0** implica
reembolso zero para a linha (hospedagem bloqueada), sem tratar como categoria
desconhecida.
**Origem:** política v4; CC-ENG-PLATAFORMA.
**Aceite:** d-010 com CC-ENG → R$ 0 (hospedagem não reembolsável). d-010 com teto
R$ 250 padrão → R$ 480 integral conforme rateio anterior.

### RN-004 — Reembolso parcial acima do limite

**Regra:** Inalterada — paga até o teto disponível (AMB-002).
**Aceite:** e-001 (representação R$ 340, teto R$ 300/dia) → R$ 300 parcial.

### RN-005 — Nota fiscal acima do limiar da política

**Regra:** Se o **valor convertido em BRL** for **estritamente maior** que
`nota_fiscal_obrigatoria_acima_de` da política e `tem_nota_fiscal` for falso → R$ 0.
**Origem:** política v4.
**Aceite:** d-003 (R$ 100 BRL, sem NF) elegível; d-004 (R$ 100,01) recusada;
e-005 (USD 40 ≈ R$ 220, sem NF) recusada.

### RN-006 — Colaborador em viagem (acréscimo percentual)

**Regra:** Nas datas “em viagem” (AMB-004), tetos de categorias com
`periodicidade` dia ou diária aumentam pelo `acrescimo_em_viagem_percentual`
da política (50 → fator 1,5) sobre o limite **efetivo do centro de custo**.
**Origem:** política v4.
**Aceite:** CC padrão alimentação R$ 60 → R$ 90 em viagem (d-011 em viagem por d-010).

### RN-007 — Competência do período

**Regra:** Inalterada.
**Aceite:** d-008 → R$ 0.

### RN-008 — Duplicatas

**Regra:** Inalterada; chave usa `valor` e demais campos **como informados**
(moeda não altera a chave).
**Aceite:** d-006/d-007.

### RN-009 — Categoria fora da política

**Regra:** Categoria normalizada **ausente** no mapa efetivo do centro de custo
→ R$ 0. Categoria presente com limite 0 (ex.: hospedagem bloqueada) **não** cai
aqui — aplica RN-003.
**Origem:** política v4.
**Aceite:** d-005 (`coworking`) → R$ 0; f-003 `representacao` com CC-SUPORTE-N2
(só padrão, sem representação) → R$ 0.

### RN-010 — Estorno (valor negativo)

**Regra:** Inalterada em espírito; margem devolvida ao saldo diário usa valores
**convertidos em BRL** na mesma (data, categoria).
**Aceite:** d-009.

### RN-011 — Arredondamento monetário

**Regra:** Duas casas decimais, half-away-from-zero, em cada valor monetário
exposto e após conversão de câmbio.
**Aceite:** d-011 → R$ 33,33.

### RN-012 — Consumo de limite diário na ordem de entrada

**Regra:** Saldo compartilhado por (data, categoria) em **BRL reembolsável**.
**Aceite:** d-001/d-002 ou equivalente CC-ENG conforme RN-001.

### RN-013 — Conversão de moeda

**Regra:** Ausência de `moeda` → `BRL`. Caso contrário, `valor_brl = valor × taxa`,
onde `taxa` vem de `cambio.json` para a **data da despesa** (AMB-016). Limites e
NF usam BRL.
**Origem:** política v4 item B.
**Aceite:** e-002 EUR 22 em 2026-07-14 (taxa 5,93) → base ≈ R$ 130,46 antes de limites.

### RN-014 — Limite diário de representação

**Regra:** Mesma lógica de RN-001/RN-012 para categoria `representacao` quando
presente no mapa efetivo (`periodicidade` = dia).
**Origem:** CC-COMERCIAL v4.
**Aceite:** e-001 cap R$ 300/dia; e-006 no mesmo dia consome saldo restante.

### RN-015 — Mapa efetivo por centro de custo

**Regra:** Parte-se de `padrao`; se `centro_custo` existir em `centros_custo`,
suas entradas **sobrescrevem** as do padrão para aquelas categorias; categorias
só no padrão permanecem; categorias só no override do CC entram no mapa.
Centro **sem** entrada em `centros_custo` usa **apenas** `padrao` (AMB-013).
**Origem:** política v4 item A.
**Aceite:** CC-SUPORTE-N2 → limites padrão; CC-ADM sem hospedagem no override
→ hospedagem continua valendo via `padrao`.

### RN-016 — Fila de aprovação manual

**Regra:** Após RN-001…RN-015, se `valor_reembolsavel` **estritamente maior**
que `aprovacao_manual_acima_de` da política (padrão R$ 500,00), o item recebe
status `pendente` em lugar de `aprovado` ou `parcial`. O valor reembolsável
calculado **não** é alterado. Itens `recusado` (R$ 0) não entram na fila.
**Origem:** comunicado v4 item C.
**Aceite:** e-007 (R$ 1.200 reembolsável) → `pendente`; e-001 (R$ 300) permanece
`parcial`; item com R$ 500,00 exatos permanece autoaprovado se demais regras OK
(AMB-020).

---

## 6. Ambiguidades identificadas e decisões

### AMB-001 — “R$ 60 por dia” — unidade do limite

**Texto original do RH:** "Alimentação tem limite de **R$ 60 por dia**."
**O que não está claro:** Limite por despesa individual ou soma de todas as
refeições na mesma data?
**Decisão:** Teto **agregado por data civil** e categoria (RN-001, RN-012); teto
numérico vem do mapa efetivo do CC (v4).
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
**Decisão:** Obrigatória apenas se valor em BRL **estritamente maior** que o limiar
da política (RN-005).
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
do limite diário da categoria na mesma data, na ordem do array (em BRL).
**Justificativa:** Estorno reflete cancelamento de gasto anterior; devolver margem
evita punir o mesmo dia.
**Regra afetada:** RN-010

### AMB-008 — Hospedagem em lançamento único (várias diárias)

**Texto original do RH:** "Hospedagem tem limite de **R$ 250 por diária**."
**O que não está claro:** Uma fatura única de várias noites — limite sobre total ou por noite?
**Decisão:** Inferir N diárias pela descrição; calcular `valor_por_diaria = valor / N`;
reembolso por diária = `min(valor_por_diaria, teto_diaria)`; somar N diárias,
limitado a `valor` (RN-003); tetos da política v4.
**Justificativa:** Política fala em “por diária”; rateio é a leitura coerente
(d-010, d-013).
**Regra afetada:** RN-003

### AMB-009 — Categoria ausente na política

**Texto original do RH:** "**Categorias fora da política não são reembolsáveis.**"
**O que não está claro:** Coworking, material, etc.
**Decisão:** Categoria ausente no **mapa efetivo** do centro de custo → R$ 0 (RN-009).
**Justificativa:** Lista fechada por CC/padrão no JSON de política.
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

### AMB-013 — “Aplica-se a política padrão”

**Texto original do RH:** centros de custo ausentes da tabela.
**O que não está claro:** Herda só tetos ou também o conjunto de categorias?
**Decisão:** Usa bloco `padrao` integralmente; override parcial só quando o CC
está listado (RN-015).
**Justificativa:** “Política padrão” no JSON é um bloco completo; CC desconhecido
não ganha categorias extras (f-003).
**Regra afetada:** RN-015, RN-009

### AMB-014 — CC com tabela parcial

**Texto original do RH:** entradas por centro incompletas.
**O que não está claro:** Categoria omitida no override — cai fora ou herda padrão?
**Decisão:** Merge: padrão + sobrescritas do CC (RN-015); omitida no override
continua valendo do padrão (CC-ADM hospedagem).
**Justificativa:** Evita buracos acidentais na política.
**Regra afetada:** RN-015

### AMB-015 — Hospedagem “não reembolsável” com limite 0

**Texto original do RH:** CC-ENG-PLATAFORMA.
**O que não está claro:** RN-009 vs teto zero.
**Decisão:** Entrada explícita com limite 0 → RN-003 (reembolso 0, categoria conhecida).
**Justificativa:** Financeiro manteve a categoria na tabela com observação.
**Regra afetada:** RN-003, RN-009

### AMB-016 — “Taxa da data da despesa” sem cotação no dia

**Texto original do RH:** câmbio + nota sobre dias úteis.
**O que não está claro:** Sábado/feriado sem PTAX.
**Decisão:** Usar a cotação da **data anterior mais recente** presente em `taxas`
(retroceder dia a dia, máx. 10 dias); se não houver → despesa recusada (R$ 0).
**Justificativa:** Alinha ao fechamento PTAX em dias úteis (e-004 sábado usa 2026-07-17).
**Regra afetada:** RN-013

### AMB-017 — Moeda sem taxa (ex.: GBP)

**Texto original do RH:** *(silêncio — e-006 GBP)*
**O que não está claro:** Comportamento quando ISO válido mas par ausente.
**Decisão:** Recusar com R$ 0 — cotação indisponível (RN-013).
**Justificativa:** Não inventar taxa; arquivo é fonte única.
**Regra afetada:** RN-013

### AMB-018 — Nota fiscal com moeda estrangeira

**Texto original do RH:** limites em BRL.
**O que não está claro:** Limiar NF compara valor informado ou convertido?
**Decisão:** Comparar **valor convertido em BRL** (RN-005).
**Justificativa:** Coerente com tetos em BRL (e-003 EUR abaixo de R$ 100).
**Regra afetada:** RN-005

### AMB-019 — `valor_informado` vs reembolso em moedas diferentes

**Texto original do RH:** *(silêncio)*
**O que não está claro:** Saída mistura moedas?
**Decisão:** `valor_informado` ecoa `valor` da entrada; `valor_reembolsavel` sempre
BRL; `status` compara reembolso ao elegível em BRL.
**Justificativa:** Empresa paga em BRL; colaborador vê o que lançou.
**Regra afetada:** RN-011, RN-013

### AMB-020 — “Passar de R$ 500” na fila manual

**Texto original do RH:** "valor reembolsável **passe de R$ 500**."
**O que não está claro:** R$ 500,00 exatos entram na fila?
**Decisão:** Pendência apenas se `valor_reembolsavel > aprovacao_manual_acima_de`
(RN-016), alinhado a AMB-003.
**Justificativa:** “Passar de” lido como estritamente acima do limiar.
**Regra afetada:** RN-016

---

## 7. Casos de borda

| Caso | Entrada (ref.) | Comportamento esperado | Regra |
|---|---|---|---|
| Duas refeições mesmo dia | d-001, d-002 | Conforme teto CC (60 ou 75) | RN-001, RN-012 |
| NF no limiar | d-003 vs d-004 | BRL; 100,00 OK; 100,01 recusa | RN-005, AMB-018 |
| Categoria proibida | d-005, e-009 | R$ 0 | RN-009 |
| Duplicata | d-006, d-007 | Inalterado | RN-008 |
| Fora competência | d-008 | R$ 0 | RN-007 |
| Estorno | d-009 | Inalterado em BRL | RN-010 |
| Hospedagem CC-ENG | d-010 | R$ 0 | RN-003, AMB-015 |
| Hospedagem multi-noite | d-010 (CC padrão) | Rateio + teto | RN-003 |
| Moeda EUR + limite | e-002 | Converter depois limitar | RN-013 |
| NF pós-conversão | e-005 | Recusa | RN-005 |
| GBP sem taxa | e-006 | R$ 0 | AMB-017 |
| Representação parcial | e-001 | R$ 300 | RN-014 |
| CC desconhecido | f-001… | Tetos padrão | RN-015 |
| Representação só comercial | f-003 | R$ 0 | RN-009 |
| Reembolso alto | e-007 | R$ 1.200, status `pendente` | RN-016 |
| Abaixo do limiar fila | e-001 | R$ 300, `parcial` (não pendente) | RN-016 |

---

## 8. Ordem de aplicação das regras

Para cada despesa, **na ordem do array** `despesas`:

1. Normalizar categoria (AMB-010).
2. Duplicata (RN-008).
3. Competência (RN-007).
4. Resolver **moeda** e **valor_brl** (RN-013); se câmbio indisponível → R$ 0.
5. Categoria no mapa efetivo (RN-009).
6. Nota fiscal sobre **valor_brl** (RN-005).
7. Estorno sobre valor_brl (RN-010).
8. Hospedagem (RN-003) ou categorias diárias — alimentação, transporte,
   representação (RN-001, RN-002, RN-014, RN-012) com RN-006.
9. Arredondar (RN-011) e status/justificativa (AMB-019).
10. **Fila manual** — se elegível e reembolso > limiar, status `pendente` (RN-016).

**Pré-processamento:** datas em viagem (AMB-004) antes dos passos 8.

---

## 9. Critérios de aceite

- [ ] CLI: `--input`, `--output`, `--politica`, `--cambio`; grava saída §4.
- [ ] `exemplos/despesas-exemplo.json` + `exemplos/envelope/politica-v4.json` +
  `exemplos/envelope/cambio.json` → resultados coerentes com RN-001…RN-015 e AMB.
- [ ] `exemplos/envelope/despesas-envelope.json` e
  `despesas-envelope-cc-desconhecido.json` processados conforme regras acima,
  incluindo RN-016 (ex.: e-007 pendente).
- [ ] Resumo: `total_reembolsavel` = soma dos itens.
- [ ] Testes automatizados por RN/AMB reconhecíveis.

---

## 10. O que fica em aberto

- **Decisão do gestor** sobre itens `pendente`: fora de escopo — o sistema só
  sinaliza a pendência.
- **Histórico de versões da política:** usa-se o arquivo informado na execução;
  vigência retroativa não altera o mecanismo.
