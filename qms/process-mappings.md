# QMS Process Mappings — Drug Quantification Framework

Structured process rules derived from NCR/CAPA records. Each entry links a
failure to the binding process rule that prevents recurrence.

## Dispatch Persistence Rule (from CAPA-2026-009 / NCR-2026-014)

**Trigger event:** ora-1 produced a 27-drug L4 clinical quantification payload
that lived only in the ephemeral session buffer; the payload was lost on lane
close and required full regeneration via a fresh lane (ora-5). Root cause:
write-required deliverable dispatched to a read-only specialist lane with no
persistence plan at dispatch time.

**Rule (binding at dispatch time):** whenever a deliverable must survive the
lane (JSON payload, report file, generated artifact), specify the persistence
mechanism BEFORE the lane is dispatched, choosing one of:

1. **Full payload in task result** — require the specialist to include the
   complete deliverable in its returned task result text (captured by the
   orchestrator before lane close); or
2. **Permitted disk path** — instruct the specialist to write the deliverable
   to a path its role may write (e.g., `%TEMP%\opencode\`); or
3. **Write-capable lane** — if neither is possible for the specialist's role
   (e.g., read-only oracle), dispatch a write-capable lane (fixer) or capture
   the payload manually at lane close.

**Gate:** verify payload capture (file exists on disk OR full text present in
the returned result) BEFORE declaring the lane reconciled. A lane whose
deliverable cannot be recovered is not complete.

**Close-time enforcement (added 2026-07-31 after recurrence NCR-2026-015):** the
Gate is a hard close gate, not guidance. Before marking any read-only lane
reconciled, confirm the required payload keys are present in the returned task
result. If the result is status-only (no payload), the lane is NOT complete:
re-dispatch with the same objective and do not close it. Status-only lane
results count as process failures (NCR).

**Applicable to:** all specialist lanes (oracle, explorer, librarian, fixer,
designer, verifier) in this framework's workflows.

## Traceability

| Rule | Origin NCR | Origin CAPA | Status |
|------|-----------|-------------|--------|
| Dispatch Persistence Rule | NCR-2026-014, NCR-2026-015 (recurrence) | CAPA-2026-009 | OPEN 2026-07-31 (reopened — close-time enforcement gate added) |
