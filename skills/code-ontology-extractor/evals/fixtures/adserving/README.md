# Ad Serving

Decides which creative to return for an incoming ad request, and settles the
resulting conversions against advertiser budgets.

The service sits behind the player's ad break. It receives an ad request,
filters the eligible creatives, ranks them and returns one. Conversions come
back asynchronously from the advertiser's tracking platform and are settled
nightly.

## Layout

- `internal/api` — HTTP entry point
- `internal/domain` — decisioning, frequency capping, settlement
- `internal/storage` — Postgres repositories
- `internal/platform` — transport and cache plumbing
