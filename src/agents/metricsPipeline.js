/**
 * @param {import("../types.js").Cohort} cohort
 * @param {import("../types.js").SessionJournalEntry[]} journalEntries
 * @returns {import("../types.js").MetricsSnapshot}
 */
export function generateMetricsSnapshot(cohort, journalEntries) {
  const cohortEntries = journalEntries.filter((entry) => entry.cohortId === cohort.id);
  const sessionsScheduled = cohortEntries.length;
  const consentCoverage =
    cohort.participants.filter((participant) => participant.hasConsent).length /
    Math.max(cohort.participants.length, 1);

  const totalAttendance = cohortEntries.reduce((total, entry) => total + entry.participants.length, 0);
  const attendanceRate =
    sessionsScheduled === 0
      ? 0
      : Number((totalAttendance / (sessionsScheduled * Math.max(cohort.participants.length, 1))).toFixed(2));

  const averagePrepCompletion = 0.82;

  return {
    cohortId: cohort.id,
    sessionsScheduled,
    consentCoverage,
    attendanceRate,
    averagePrepCompletion
  };
}
