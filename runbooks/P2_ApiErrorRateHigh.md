# Runbook P2 - ApiErrorRateHigh

## Alerte
- Nom: `ApiErrorRateHigh`
- Source: Prometheus
- Priorite: `P2`

## Impact
- Degradation de l'experience patient.
- Echecs de paiement et pertes de facturation.
- Risque de surcharge support.

## Diagnostic
1. Verifier dashboard RED:
   - taux d'erreur 5xx
   - endpoint impacte
   - latence p95
2. Verifier logs applicatifs dans Kibana pour endpoint fautif.
3. Verifier disponibilite des dependances MySQL/Redis.
4. Verifier capacite API (dashboard HA) et pression infra (USE).

## Resolution
1. Si endpoint `/api/payment` uniquement: confirmer que le taux reste proche de la simulation attendue.
2. Si depassement reel:
   - redemarrer instances API impactees
   - reduire charge temporairement si necessaire
   - corriger bug applicatif puis redeployer
3. Verifier retour sous seuil:
   - `ApiErrorRateHigh` resolue
   - p95 et taux 5xx stabilises

## Escalade
- Si 5xx > 10% pendant 10 min: passer en P1.
- Si paiement indisponible: escalation produit + metier immediate.

## Checklist post-mortem
- Endpoint fautif identifie
- Correctif code ou infra trace
- Test de non-regression ajoute
- Seuils d'alerte reevalues
