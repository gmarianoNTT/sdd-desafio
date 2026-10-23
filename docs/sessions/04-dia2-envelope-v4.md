# Sessão 04 — Dia 2 envelope (Política v4)

**Data:** 2026-10-23

## Resumo

- Spec atualizada para v2.0 (RN-013…015, AMB-013…019).
- D-002 em `DECISIONS.md`.
- Fase 5 tasks T-019…T-025 implementadas.
- Política e câmbio externos; CLI `--politica` / `--cambio`.
- Item C (aprovação > R$ 500) não implementado (fora de escopo).

## Arquivos principais

- `exemplos/envelope/*`
- `src/reembolso/motor/politica_config.py`, `cambio.py`, `calcular.py`
- `src/reembolso/io/politica_io.py`, `cambio_io.py`
- `tests/test_envelope_v4.py`, `test_rn_013.py`

## Notas para relatório

- `centro_custo` deixou de ser decorativo — exigiu refactor do núcleo.
- CC-ENG altera regressão do JSON de exemplo (d-010 hospedagem R$ 0).
- GBP sem cotação → recusa (e-006).
