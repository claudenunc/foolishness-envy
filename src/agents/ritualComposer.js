/** @param {import("../types.js").Cohort} cohort */
export function composeRitualAssets(cohort) {
  return {
    introTrack: cohort.ritualProfile.introTrack,
    outroTrack: cohort.ritualProfile.outroTrack,
    prompts: cohort.ritualProfile.prompts,
    hostMessage: cohort.ritualProfile.hostMessage
  };
}

/** @param {import("../types.js").ScheduledSession} session */
export function craftPrepDigest(session) {
  const agenda = [
    "Welcome ritual & sound check",
    "Collective pulse check",
    "Creative collaboration breakout",
    "Commitment circle & close"
  ];

  const personalizedNotes = {};
  session.participants.forEach((participant) => {
    personalizedNotes[participant.id] = `Hey ${participant.name}, bring one artifact that captured your energy this week.`;
  });

  const ritualPrompt = session.ritual.prompts[0] ?? "Share one win since our last convening.";

  return {
    agenda,
    personalizedNotes,
    ritualPrompt
  };
}
