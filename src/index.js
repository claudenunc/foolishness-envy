import { orchestrateAutomaticZoom } from "./workflows/orchestrateAutomaticZoom.js";
import { sampleCohorts } from "./data/sampleCohorts.js";
import { toIsoNoSeconds } from "./utils/date.js";

async function bootstrap() {
  console.log("Bootstrapping Automatic Zoom MVP...\n");
  const result = await orchestrateAutomaticZoom(sampleCohorts);

  console.log("=== Scheduled Sessions ===");
  result.scheduledSessions.forEach((session) => {
    console.log(`${session.cohortId} -> ${toIsoNoSeconds(session.start)} to ${toIsoNoSeconds(session.end)}`);
    console.log(`Zoom: ${session.zoomDetails.joinUrl}`);
    console.log(`Agenda: ${session.prepDigest.agenda.join(" | ")}`);
    console.log("");
  });

  console.log("=== Compliance ===");
  result.complianceReports.forEach((report) => {
    console.log(`${report.cohortId}: ${(report.consentCoverage * 100).toFixed(0)}% consent coverage`);
    if (!report.compliant) {
      report.issues.forEach((issue) => {
        console.log(` - ${issue.participant.name}: ${issue.reason}`);
      });
    }
  });

  console.log("\n=== Metrics ===");
  result.metrics.forEach((metric) => {
    console.log(`${metric.cohortId}: sessions=${metric.sessionsScheduled}, attendance=${metric.attendanceRate}`);
  });

  console.log("\n=== Host Reminders ===");
  result.hostReminders.forEach((reminder) => {
    console.log(reminder);
    console.log("----------------");
  });
}

bootstrap().catch((error) => {
  console.error("Automatic Zoom orchestration failed", error);
  process.exit(1);
});
