import { randomUUID } from "crypto";
import { addMinutes, availabilityEngulfs, parseISO } from "../utils/date.js";

/** @typedef {import("../types.js").Cohort} Cohort */
/** @typedef {import("../types.js").ScheduledSession} ScheduledSession */

const DEFAULT_LOOKAHEAD_DAYS = 14;
const MINIMUM_CONSENT_COVERAGE = 0.9;

function isWithinLookahead(date, lookAheadDays) {
  const now = new Date();
  const boundary = addMinutes(now, lookAheadDays * 24 * 60);
  return date.getTime() >= now.getTime() && date.getTime() <= boundary.getTime();
}

/**
 * @param {Cohort} cohort
 * @param {{ lookAheadDays?: number; minimumConsentCoverage?: number }} [options]
 * @returns {ScheduledSession[]}
 */
export function scheduleCohortSessions(cohort, options = {}) {
  const lookAheadDays = options.lookAheadDays ?? DEFAULT_LOOKAHEAD_DAYS;
  const minimumConsentCoverage = options.minimumConsentCoverage ?? MINIMUM_CONSENT_COVERAGE;

  const consented = cohort.participants.filter((participant) => participant.hasConsent);
  if (consented.length === 0) {
    return [];
  }

  const candidateWindows = consented.flatMap((participant) => participant.availability);
  const sortedWindows = candidateWindows
    .map((window) => ({ ...window, start: parseISO(window.start), end: parseISO(window.end) }))
    .filter((window) => isWithinLookahead(window.start, lookAheadDays))
    .sort((a, b) => a.start.getTime() - b.start.getTime());

  for (const window of sortedWindows) {
    const sessionStart = window.start;
    const sessionEnd = addMinutes(sessionStart, cohort.sessionLengthMinutes);
    if (sessionEnd.getTime() > window.end.getTime()) {
      continue;
    }

    const potentialParticipants = cohort.participants.filter((participant) => {
      return participant.availability.some((availability) => {
        const availabilityStart = parseISO(availability.start);
        const availabilityEnd = parseISO(availability.end);
        return availabilityEngulfs(availabilityStart, availabilityEnd, sessionStart, sessionEnd);
      });
    });

    if (potentialParticipants.length === 0) {
      continue;
    }

    const consentCoverage =
      potentialParticipants.filter((participant) => participant.hasConsent).length /
      potentialParticipants.length;
    if (consentCoverage < minimumConsentCoverage) {
      continue;
    }

    /** @type {ScheduledSession} */
    const scheduledSession = {
      cohortId: cohort.id,
      sessionId: randomUUID(),
      start: sessionStart,
      end: sessionEnd,
      participants: potentialParticipants,
      zoomDetails: {
        meetingId: "",
        joinUrl: "",
        hostUrl: "",
        passcode: ""
      },
      ritual: {
        introTrack: cohort.ritualProfile.introTrack,
        outroTrack: cohort.ritualProfile.outroTrack,
        prompts: cohort.ritualProfile.prompts,
        hostMessage: cohort.ritualProfile.hostMessage
      },
      prepDigest: {
        agenda: [],
        personalizedNotes: {},
        ritualPrompt: ""
      }
    };

    return [scheduledSession];
  }

  return [];
}
