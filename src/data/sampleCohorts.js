/** @typedef {import("../types.js").Cohort} Cohort */

function isoDaysAhead(daysAhead, hour, durationHours) {
  const base = new Date();
  base.setUTCHours(0, 0, 0, 0);
  base.setUTCDate(base.getUTCDate() + daysAhead);
  const start = new Date(base.getTime());
  start.setUTCHours(hour, 0, 0, 0);
  const end = new Date(start.getTime() + durationHours * 60 * 60 * 1000);
  return { start: start.toISOString(), end: end.toISOString() };
}

/** @type {Cohort[]} */
export const sampleCohorts = [
  {
    id: "cohort-education",
    name: "Agent Academy Sprint",
    program: "education",
    sessionLengthMinutes: 75,
    preferredChannels: ["email", "discord"],
    ritualProfile: {
      introTrack: "skellington:intro:rebirth",
      outroTrack: "skellington:outro:ascend",
      prompts: [
        "What liberation did you feel experimenting with today's agent ritual?",
        "Name one human you want to uplift this week."
      ],
      hostMessage: "We are here to rehearse the future. Arrive hydrated, present, and ready to co-create."
    },
    participants: [
      {
        id: "participant-1",
        name: "Nova",
        timezone: "America/Los_Angeles",
        email: "nova@example.com",
        discordHandle: "nova#1234",
        hasConsent: true,
        availability: [isoDaysAhead(3, 19, 3), isoDaysAhead(5, 18, 3)]
      },
      {
        id: "participant-2",
        name: "Orion",
        timezone: "America/New_York",
        email: "orion@example.com",
        hasConsent: true,
        availability: [isoDaysAhead(3, 21, 2), isoDaysAhead(7, 19, 3)]
      },
      {
        id: "participant-3",
        name: "Lyra",
        timezone: "Europe/London",
        email: "lyra@example.com",
        hasConsent: false,
        availability: [isoDaysAhead(3, 18, 2.5), isoDaysAhead(8, 17, 2)]
      }
    ]
  },
  {
    id: "cohort-artist",
    name: "Skellington Studio Lab",
    program: "artist",
    sessionLengthMinutes: 60,
    preferredChannels: ["email", "sms"],
    ritualProfile: {
      introTrack: "skellington:intro:pulse",
      outroTrack: "skellington:outro:embers",
      prompts: [
        "Which sound unlocked a new emotion for you this week?",
        "Drop a lyric that reflects our collective mood."
      ],
      hostMessage: "We respect the ancestors and the algorithms. Bring your most daring demo."
    },
    participants: [
      {
        id: "participant-4",
        name: "Maya",
        timezone: "America/Chicago",
        email: "maya@example.com",
        phone: "+13125550123",
        hasConsent: true,
        availability: [isoDaysAhead(4, 18, 2), isoDaysAhead(8, 17, 3)]
      },
      {
        id: "participant-5",
        name: "Zephyr",
        timezone: "America/Los_Angeles",
        email: "zephyr@example.com",
        phone: "+14155550123",
        hasConsent: true,
        availability: [isoDaysAhead(4, 19, 2), isoDaysAhead(8, 18, 2)]
      }
    ]
  }
];
