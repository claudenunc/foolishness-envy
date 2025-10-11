/**
 * Parse an ISO8601 timestamp into a Date instance.
 * @param {string} iso
 * @returns {Date}
 */
export function parseISO(iso) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) {
    throw new Error(`Invalid ISO timestamp: ${iso}`);
  }
  return date;
}

/**
 * Add minutes to a Date and return a new Date.
 * @param {Date} date
 * @param {number} minutes
 * @returns {Date}
 */
export function addMinutes(date, minutes) {
  return new Date(date.getTime() + minutes * 60_000);
}

/**
 * Calculate the difference in minutes between two dates.
 * @param {Date} start
 * @param {Date} end
 * @returns {number}
 */
export function differenceInMinutes(start, end) {
  return (end.getTime() - start.getTime()) / 60_000;
}

/**
 * Format a Date as an ISO string without seconds for human-readable output.
 * @param {Date} date
 * @returns {string}
 */
export function toIsoNoSeconds(date) {
  return date.toISOString().replace(/:\d{2}\.\d{3}Z$/, "Z");
}

/**
 * Determine if an availability window fully contains a proposed session window.
 * @param {Date} availabilityStart
 * @param {Date} availabilityEnd
 * @param {Date} sessionStart
 * @param {Date} sessionEnd
 * @returns {boolean}
 */
export function availabilityEngulfs(availabilityStart, availabilityEnd, sessionStart, sessionEnd) {
  return availabilityStart.getTime() <= sessionStart.getTime() && availabilityEnd.getTime() >= sessionEnd.getTime();
}
