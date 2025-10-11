/**
 * @param {import("../types.js").Cohort} cohort
 * @returns {{ cohortId: string; compliant: boolean; consentCoverage: number; issues: { participant: import("../types.js").Participant; reason: string; }[] }}
 */
export function evaluateConsent(cohort) {
  const issues = [];
  const total = cohort.participants.length;
  const withConsent = cohort.participants.filter((participant) => {
    if (participant.hasConsent) {
      return true;
    }
    issues.push({ participant, reason: "Missing consent acknowledgement" });
    return false;
  }).length;

  const consentCoverage = total === 0 ? 0 : withConsent / total;

  return {
    cohortId: cohort.id,
    compliant: consentCoverage >= 0.9,
    consentCoverage,
    issues
  };
}
