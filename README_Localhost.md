# Localhost Development Setup

## Quick Start

1. Run the local development server:
```bash
cd /home/sub-acct/Hey-Big-Proppa/backend && source ../.venv/bin/activate && python -m uvicorn main:app --host 0.0.0.0 --port 8010
```

2. Open your browser to:
- http://localhost:8010 (main app)
- http://localhost:8010/api (API documentation)

## What's Included

When you run the local server, you'll have:
- All 438 player pages with slug URLs (e.g., `/p/202611121643-tua-tagovailoa-mia`)
- Jimmy's Take for every player with zero contradictions
- Complete player dimension data with 7,210 players including name-resolved GSIS IDs
- Mock ESPN API endpoints that use the lake data
- All bug fixes applied:
  - Wrong-market guards for kickers/linemen
  - Name-integrity guards for anonymous players
  - Call authority: flags > lake edge > composite
  - Connection pooling and proper cache invalidation
  - Fixed grammar bugs in Jimmy's voice

## Development Workflow

- Frontend code: `frontend/src/`
- Backend code: `backend/`
- Lake data: `lake/gold/nfl/` (tracked) and `lake/gold/espn/` (tracked now)
- Rebuild Jimmy's takes: `python scripts/seed_jimmy_takes.py`
- Update player names: `python scripts/resolve_player_names.py`
- Refresh data without restart: Hit `/api/refresh-data`

## Testing

After starting the server, try these URLs:
- Main app: http://localhost:8010
- A specific player page: http://localhost:8010/p/202611121643-tua-tagovailoa-mia
- API endpoint: http://localhost:8010/api/chart/player_props?player_id=00-0036212&market=rushyds
- Slug resolve: http://localhost:8010/api/slug/resolve/202611121643-jimmy-garoppolo-rai

## Troubleshooting

If you encounter issues:
1. Check that all requirements are installed: `pip install -r requirements.txt`
2. Verify Node.js is accessible: 
   ```bash
   export PATH="$HOME/Downloads/node-v26.13.1-linux-x64/bin:$PATH"
   node --version
   ```
3. Check that the frontend built successfully: `ls -la frontend/dist`
4. Verify player dimension data loads correctly by visiting `/api/dimension`