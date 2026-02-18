# Runbook P1 - MysqlBackupFailed

## Alerte
- Nom: `MysqlBackupFailed`
- Source: Prometheus via Pushgateway metrics
- Priorite: `P1`

## Impact
- Donnees medicales non proteges en cas de sinistre.
- Risque legal et conformite eleve.
- RPO de 30 minutes non garanti.

## Diagnostic
1. Verifier l'etat de MySQL:
   - `docker compose ps mysql`
   - `docker compose logs --tail=200 mysql`
2. Verifier execution backup:
   - `docker compose run --rm --no-deps traffic sh -lc "echo test"`
   - execution reelle du script backup selon procedure equipe.
3. Verifier metriques Pushgateway:
   - `curl http://localhost:9091/metrics | findstr mysql_backup`
4. Verifier espace disque sur l'hote.

## Resolution
1. Corriger acces MySQL (host, user, password, privileges).
2. Relancer un backup manuel:
   - `bash backup/backup.sh` (depuis environnement qui resout `mysql` et `pushgateway`)
3. Verifier:
   - `mysql_backup_status 0`
   - `mysql_backup_last_timestamp` recent
4. Confirmer alerte resolue dans Alertmanager.

## Escalade
- Si echec > 30 min: escalade P1 vers responsable exploitation.
- Si echec repete > 3 occurrences/24h: ouvrir incident majeur.

## Checklist post-mortem
- Cause racine documentee
- Test de restauration effectue
- RPO/RTO revalide
- Correctif automatise planifie
