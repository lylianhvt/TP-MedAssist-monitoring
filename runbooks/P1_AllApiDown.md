# Runbook P1 - AllApiDown

## Alerte
- Nom: `AllApiDown`
- Source: Prometheus via Alertmanager
- Priorite: `P1`

## Impact
- Patients: impossibilite de prendre rendez-vous et de payer.
- Medecins: interruptions de consultations en cours.
- Metier: perte immediate de revenu et risque de non-conformite.

## Diagnostic
1. Verifier l'alerte dans Alertmanager.
2. Verifier la sante HAProxy: `http://localhost:8404/stats`.
3. Verifier les conteneurs API:
   - `docker compose ps api api2 api3 haproxy`
   - `docker compose logs --tail=200 api api2 api3 haproxy`
4. Verifier dependances:
   - `docker compose ps mysql redis`
   - `docker compose logs --tail=200 mysql redis`

## Resolution
1. Redemarrer dans cet ordre:
   - `docker compose up -d mysql redis`
   - `docker compose up -d api api2 api3`
   - `docker compose up -d haproxy`
2. Valider la reprise:
   - `curl http://localhost:8081/health`
   - `curl http://localhost:8081/api/payment`
3. Verifier retour des metriques:
   - Prometheus targets `UP`
   - Dashboard HA: 3 backends actifs

## Escalade
- Si indisponibilite > 10 min: escalade immediate incident manager.
- Si recurrent sur 24h: ouverture post-mortem obligatoire avec lead dev + ops.

## Checklist post-mortem
- Cause racine identifiee
- MTTD / MTTR mesures
- Actions correctives avec owner et date
- Verification monitoring et alertes mise a jour
