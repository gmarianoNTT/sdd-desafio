# Sessão 02 — Dia 1 manhã (documentação)
_Export alternativo (Cursor) — 2026-10-18_

---

## Objetivo

Fechar `spec.md`, `plan.md` e `tasks.md` antes de implementar código, conforme
cronograma do desafio SDD.

## Decisões principais (spec)

- Limites diários **agregados por data** (AMB-001), consumo na **ordem do array** (RN-012).
- Reembolso **parcial** até o teto, não recusa total do item (AMB-002).
- NF obrigatória só se `valor > 100` (AMB-003).
- **Em viagem** inferido por intervalo de hospedagem parseado da descrição (AMB-004).
- Duplicata: mesma data/categoria/fornecedor/valor/descrição; mantém a primeira (AMB-005).
- Estorno: R$ 0 reembolsável, devolve saldo diário (AMB-007).
- Hospedagem: rateio `valor/N` diárias com regex na descrição (AMB-008).
- Stack escolhida no plan: Python 3.11, pytest, Decimal, CLI `reembolso calcular`.

## Artefatos produzidos

- `specs/001-motor-reembolso/spec.md` v1.0 (12 AMB, RN-001…RN-012)
- `specs/001-motor-reembolso/plan.md` v1.0
- `specs/001-motor-reembolso/tasks.md` (T-001…T-018 + matriz de cobertura)
- `CLAUDE.md` atualizado com stack/comandos

## Próximo passo (tarde Dia 1)

Implementar T-001 em diante; ainda sem `src/` no repositório.
