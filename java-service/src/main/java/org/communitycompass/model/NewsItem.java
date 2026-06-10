package org.communitycompass.model;

/**
 * A weekly community update / civic-guidance item (CC-15), modeled on
 * FirstStep's NewsItem. {@code whyItMatters} is the plain-language explanation
 * (CC-16) that tells a resident how an update affects them.
 *
 * <p>A Java record gives us an immutable value type with JSON serialization for
 * free (Jackson handles records out of the box).
 */
public record NewsItem(
        String id,
        String headline,
        String summary,
        String category,     // housing | food | health | employment | benefits ...
        String urgency,      // low | medium | high
        String published,    // ISO date
        String deadline,     // ISO date or null
        String source,
        String whyItMatters  // CC-16 plain-language briefing
) {}
