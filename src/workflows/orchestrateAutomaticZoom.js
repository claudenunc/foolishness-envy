import { scheduleCohortSessions } from "../agents/schedulingAgent.js";
import { provisionZoomMeeting } from "../agents/zoomAdapter.js";
import { composeRitualAssets, craftPrepDigest } from "../agents/ritualComposer.js";
import { evaluateConsent } from "../agents/complianceGuard.js";
import { synthesizeInsights } from "../agents/insightSynthesizer.js";
import { buildNotificationPayloads, formatHostReminder } from "../agents/notificationAgent.js";
import { generateMetricsSnapshot } from "../agents/metricsPipeline.js";

/**
 * @param {import("../types.js").Cohort[]} cohorts
 * @returns {Promise<{
 *  scheduledSessions: import("../types.js").ScheduledSession[];
 *  sessionJournal: import("../types.js").SessionJournalEntry[];
 *  hostReminders: string[];
 *  metrics: import("../types.js").MetricsSnapshot[];
 *  complianceReports: ReturnType<typeof evaluateConsent>[];
 * }>}
 */
export async function orchestrateAutomaticZoom(cohorts) {
  const scheduledSessions = [];
  const sessionJournal = [];
  const hostReminders = [];
  const complianceReports = cohorts.map((cohort) => evaluateConsent(cohort));

  for (const cohort of cohorts) {
    const scheduled = scheduleCohortSessions(cohort);
    for (const session of scheduled) {
      const zoomDetails = await provisionZoomMeeting(session, {
        vanityUrl: "https://zoom.foolishness.envy"
      });
      session.zoomDetails = zoomDetails;
      session.ritual = composeRitualAssets(cohort);
      session.prepDigest = craftPrepDigest(session);

      const notificationPayloads = buildNotificationPayloads(cohort, session);
      const hostReminder = formatHostReminder(session);

      const insights = synthesizeInsights(session);
      const journalEntry = {
        sessionId: session.sessionId,
        cohortId: cohort.id,
        start: session.start,
        end: session.end,
        zoomMeeting: zoomDetails,
        participants: session.participants.map((participant) => participant.id),
        consentVerified: complianceReports.find((report) => report.cohortId === cohort.id)?.compliant ?? false,
        insights
      };

      scheduledSessions.push(session);
      sessionJournal.push(journalEntry);
      hostReminders.push(hostReminder);

      console.log("--- Notifications ---");
      notificationPayloads.forEach((payload) => {
        console.log(`[${payload.channel}] -> ${payload.recipient.name}: ${payload.message}`);
      });
      console.log("---------------------\n");
    }
  }

  const metrics = cohorts.map((cohort) => generateMetricsSnapshot(cohort, sessionJournal));

  return {
    scheduledSessions,
    sessionJournal,
    hostReminders,
    metrics,
    complianceReports
  };
}
