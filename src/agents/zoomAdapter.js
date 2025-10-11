import { randomUUID } from "crypto";

const ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789";

function generatePasscode(length) {
  let passcode = "";
  for (let index = 0; index < length; index += 1) {
    const randomIndex = Math.floor(Math.random() * ALPHABET.length);
    passcode += ALPHABET[randomIndex];
  }
  return passcode;
}

/**
 * @param {import("../types.js").ScheduledSession} session
 * @param {{ vanityUrl?: string; passcodeLength?: number }} [config]
 * @returns {Promise<import("../types.js").ZoomMeeting>}
 */
export async function provisionZoomMeeting(session, config = {}) {
  const vanityUrl = config.vanityUrl ?? "https://zoom.us";
  const passcodeLength = config.passcodeLength ?? 6;

  const meetingId = randomUUID();
  const passcode = generatePasscode(passcodeLength);

  await new Promise((resolve) => setTimeout(resolve, 25));

  return {
    meetingId,
    joinUrl: `${vanityUrl}/j/${meetingId}?pwd=${passcode}`,
    hostUrl: `${vanityUrl}/host/${meetingId}`,
    passcode
  };
}
