/**
 * @param {import("../types.js").ScheduledSession} session
 * @returns {import("../types.js").SessionInsights}
 */
export function synthesizeInsights(session) {
  const prompts = session.ritual.prompts;
  const keyMoments = [
    `Collective reflection on: "${prompts[0] ?? "How did we grow?"}"`,
    "Breakout remix: 3 unexpected collaborations formed"
  ];

  const followUpActions = [
    "Share session recording and highlight reel",
    "Assign co-creation tasks to next convening leads",
    "Update Agent OS backlog with emergent feature requests"
  ];

  return {
    sessionId: session.sessionId,
    keyMoments,
    followUpActions,
    sentiment: "celebratory"
  };
}
