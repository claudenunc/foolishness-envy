# Foolishness eNVy Automatic Zoom MVP

This repository contains the Build 11 Automatic Zoom coordination MVP. It models the agents, workflows, and data contracts required to automate ritual-driven Zoom convenings across the FooLiSHNeSS eNVy portfolio.

## Getting Started

```bash
npm install # no external dependencies, installs package metadata only
npm run start
```

The startup script orchestrates the complete workflow for two sample cohorts, printing notifications, compliance status, metrics, and host reminders.

## Project Structure

- `src/types.js` – shared JSDoc typings spanning cohorts, sessions, rituals, and analytics.
- `src/utils/date.js` – lightweight date helpers for scheduling logic.
- `src/data/sampleCohorts.js` – representative cohort data to exercise the orchestration.
- `src/agents/` – domain-specific agents that encapsulate scheduling, compliance, rituals, insights, notifications, and metrics.
- `src/workflows/orchestrateAutomaticZoom.js` – coordinates the agents into an end-to-end flow.
- `src/index.js` – entry point that runs the orchestration and logs deliverables.

## Next Steps

- Replace mock Zoom provisioning with authenticated API calls.
- Persist the session journal and metrics snapshots to Supabase.
- Wire the notification payloads into Postmark, Twilio, and Discord webhooks.
- Expand the Scheduling Agent to support recurring cadences and human override queueing.
- Connect Insight Synthesizer to real transcription data and sentiment analysis APIs.
