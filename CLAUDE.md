# VedicJivan — Claude Instructions

## Git Workflow (STRICT RULE)
- **NEVER push directly to `main`**
- Always push to `staging` first
- Test on the staging environment (`vedicjivan-test.nandishdave.world`)
- Only merge `staging` → `main` once everything is confirmed working

## Branch → Environment mapping
- `staging` → test env at `vedicjivan-test.nandishdave.world`
- `main` → production at `vedicjivan.nandishdave.world`
