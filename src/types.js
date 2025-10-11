/**
 * @typedef {"email" | "sms" | "discord"} Channel
 */

/**
 * @typedef {Object} AvailabilityWindow
 * @property {string} start ISO8601 start timestamp
 * @property {string} end ISO8601 end timestamp
 */

/**
 * @typedef {Object} Participant
 * @property {string} id
 * @property {string} name
 * @property {string} timezone
 * @property {string} email
 * @property {string=} phone
 * @property {string=} discordHandle
 * @property {boolean} hasConsent
 * @property {AvailabilityWindow[]} availability
 */

/**
 * @typedef {Object} RitualProfile
 * @property {string} introTrack
 * @property {string} outroTrack
 * @property {string[]} prompts
 * @property {string} hostMessage
 */

/**
 * @typedef {Object} Cohort
 * @property {string} id
 * @property {string} name
 * @property {"education" | "artist" | "community"} program
 * @property {number} sessionLengthMinutes
 * @property {Channel[]} preferredChannels
 * @property {Participant[]} participants
 * @property {RitualProfile} ritualProfile
 */

/**
 * @typedef {Object} ZoomMeeting
 * @property {string} meetingId
 * @property {string} joinUrl
 * @property {string} hostUrl
 * @property {string} passcode
 */

/**
 * @typedef {Object} RitualAssets
 * @property {string} introTrack
 * @property {string} outroTrack
 * @property {string[]} prompts
 * @property {string} hostMessage
 */

/**
 * @typedef {Object} PrepDigest
 * @property {string[]} agenda
 * @property {Object.<string, string>} personalizedNotes
 * @property {string} ritualPrompt
 */

/**
 * @typedef {Object} ScheduledSession
 * @property {string} cohortId
 * @property {string} sessionId
 * @property {Date} start
 * @property {Date} end
 * @property {Participant[]} participants
 * @property {ZoomMeeting} zoomDetails
 * @property {RitualAssets} ritual
 * @property {PrepDigest} prepDigest
 */

/**
 * @typedef {Object} SessionInsights
 * @property {string} sessionId
 * @property {string[]} keyMoments
 * @property {string[]} followUpActions
 * @property {"celebratory" | "reflective" | "urgent"} sentiment
 */

/**
 * @typedef {Object} SessionJournalEntry
 * @property {string} sessionId
 * @property {string} cohortId
 * @property {Date} start
 * @property {Date} end
 * @property {ZoomMeeting} zoomMeeting
 * @property {string[]} participants
 * @property {boolean} consentVerified
 * @property {SessionInsights} insights
 */

/**
 * @typedef {Object} MetricsSnapshot
 * @property {string} cohortId
 * @property {number} sessionsScheduled
 * @property {number} consentCoverage
 * @property {number} attendanceRate
 * @property {number} averagePrepCompletion
 */

/**
 * @typedef {Object} NotificationPayload
 * @property {Channel} channel
 * @property {Participant} recipient
 * @property {string} message
 */

export {};
