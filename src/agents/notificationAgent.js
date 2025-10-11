import { toIsoNoSeconds } from "../utils/date.js";

/**
 * @param {import("../types.js").Channel} channel
 * @param {import("../types.js").ScheduledSession} session
 */
function buildMessage(channel, session) {
  const startIso = toIsoNoSeconds(session.start);
  const base = `Session for ${session.cohortId} on ${startIso}`;
  switch (channel) {
    case "discord":
      return `${base}\n${session.ritual.hostMessage}`;
    case "sms":
      return `${base}. Passcode ${session.zoomDetails.passcode}.`;
    default:
      return `${base}\nAgenda: ${session.prepDigest.agenda.join(" → ")}`;
  }
}

/**
 * @param {import("../types.js").Cohort} cohort
 * @param {import("../types.js").ScheduledSession} session
 * @returns {import("../types.js").NotificationPayload[]}
 */
export function buildNotificationPayloads(cohort, session) {
  return cohort.preferredChannels.flatMap((channel) => {
    return session.participants.map((participant) => ({
      channel,
      recipient: participant,
      message: buildMessage(channel, session)
    }));
  });
}

/**
 * @param {import("../types.js").ScheduledSession} session
 */
export function formatHostReminder(session) {
  const start = toIsoNoSeconds(session.start);
  return [
    `Host Command Center: ${session.zoomDetails.hostUrl}`,
    `Start time: ${start}`,
    `Ritual prompt: ${session.prepDigest.ritualPrompt}`,
    `Participants: ${session.participants.map((participant) => participant.name).join(", ")}`
  ].join("\n");
}
