# Motor de reembolso de despesas

CLI que lê um JSON de despesas corporativas e grava o resultado do cálculo de reembolso (valor reembolsável, status e justificativa por item), conforme a política documentada em `specs/001-motor-reembolso/spec.md`.

## Requisitos

- Python 3.11 ou superior

## Instalação

```bash
python -m pip install -e .
```

## Uso

```bash
reembolso calcular \
  --input exemplos/despesas-exemplo.json \
  --output resultado.json \
  --politica exemplos/envelope/politica-v4.json \
  --cambio exemplos/envelope/cambio.json
```

Alternativa sem entry point no PATH:

```bash
python -m reembolso.cli.main calcular \
  --input exemplos/despesas-exemplo.json \
  --output resultado.json \
  --politica exemplos/envelope/politica-v4.json \
  --cambio exemplos/envelope/cambio.json
```

Exemplos do envelope (Dia 2): `exemplos/envelope/despesas-envelope.json` e
`despesas-envelope-cc-desconhecido.json` com os mesmos `--politica` e `--cambio`.

## Testes

```bash
python -m pip install -e . pytest
python -m pytest
```

## Documentação do desafio

- **Spec (regras de negócio):** `specs/001-motor-reembolso/spec.md`
- **Plano técnico:** `specs/001-motor-reembolso/plan.md`
- **Tasks:** `specs/001-motor-reembolso/tasks.md`
- **Decisões de spec:** `specs/001-motor-reembolso/DECISIONS.md`

## Estrutura

```
src/reembolso/
  cli/          # argparse e comando calcular
  io/           # leitura/escrita JSON
  motor/        # núcleo puro (regras RN-001…)
tests/          # testes por RN/AMB e integração
```
