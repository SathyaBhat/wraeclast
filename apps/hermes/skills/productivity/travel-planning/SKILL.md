---
name: travel-planning
description: Use when planning trips or scenic day drives. Compare, verify live, recommend one.
---

# Travel Planning

Use for multi-day leisure trips where the user wants a concrete shortlist, day-by-day rhythm, pricing realism, and optionally a note saved to their planning system. Also covers **scenic day drives** from home (see the section below).

## Scenic day drives from home

1. **Check what the user has already done first.** Read `references/sydney-day-drives.md` for drives already covered and excluded. The user has done the standard Sydney day trips, so leading with them wastes rounds. Lead with lesser-known roads and destinations.
2. **Prioritise the road over the destination.** When the user asks for curvy roads or rolling hills, rank options by driving quality: corners, traffic, scenery. Then name the stops. Prefer loops over out-and-back routes.
3. **Resolve which option a follow-up refers to.** After offering several drives, read a follow-up like "check what's available there" as being about the option you recommended. If that's unclear, ask with clarify. Don't pick a different option silently.
4. **Verify stops live for the travel day.** Check the regional tourism "what's on" page for that date, and the venue's own site or Facebook page for opening hours. Weekday-only attractions are a common trap. Mark anything unconfirmed.
5. **EV logistics:** say whether the round trip fits the EV's range. Flag remote routes with sparse chargers or no mobile coverage.
6. **Answer format:** a short list of 2–4 options. Give each one its route, why the driving is good, specific stops, and caveats, then end with one pick. Present sourced facts plainly and label training-knowledge claims as unverified.

## Workflow

1. **Fix the planning assumptions.** State assumed dates, party size, origin, currency, number of nights, desired pace, and what the stated budget includes. If dates are vague but a seasonal period is named, use a representative date range and label it an assumption.
2. **Start with the user’s requested hotel group or loyalty ecosystem.** Identify the properties that actually match the destination and the user’s desired mood; do not treat every branded property as equally suitable.
3. **Validate live availability for the representative dates.** Prefer bookable rate pages that show date-specific rooms, inclusions, taxes, cancellation terms, and inventory. Official property pages are best for amenities and transfer details, but can be bot-blocked; use a reputable OTA as a price cross-check when needed.
4. **Compare the true nightly cost.** Include displayed taxes and convert into the user’s currency using a cited current/reference FX rate. Call out exclusions: transfers, resort fees, mandatory festive meals, breakfast, and package inclusions. Use a calculation tool rather than doing arithmetic mentally.
5. **Assess airport-to-resort friction.** Note direct-flight duration, airport transfer time, boats/ferries/internal flights, departure buffers, and weather exposure. For a short, relaxation-first trip, transfer complexity can outweigh a modest room saving.
6. **Make one recommendation, then two bounded alternatives.** Explain fit against the user’s mood and budget. Avoid a sprawling list.
7. **Design a deliberately sparse itinerary.** For relaxation trips, leave most afternoons unscheduled; include one optional active day and a protected arrival/departure buffer.
8. **Document findings with retrieval date and source links.** If the user asks for a wiki update, save a self-contained note and add it to the relevant index.

## Pricing discipline

- Label all live rates as a **snapshot** and preserve the searched dates, room, guest count, currency, taxes and cancellation condition.
- Do not describe a non-peak airfare as a Christmas price. If exact peak inventory is unavailable, label any fare only as a non-peak indicator.
- Holiday periods may impose festive meals or blackout package dates. Treat those as material costs until confirmed.
- A room that technically meets the nightly cap before transfers or mandatory festive supplements does not fully meet the budget; make that distinction explicit.

## Sources and fallback pattern

- Use direct carrier pages for route duration and fare context, property/brand pages for facilities and access, and date-specific OTA results for live comparison pricing.
- If hotel brand pages fail to render or block scraping, do not repeatedly retry the same path. Switch source type and preserve which source supplied each claim.
- Treat OTA descriptions as useful operational evidence but verify property-level claims against brand pages or a second source when practical.

## Activity fit and novice safety

When the user is new to an activity (for example, snorkelling), recommend a guided, beginner-friendly format—not the technically hardest or most independent version. Before presenting it as bookable, verify or explicitly ask the operator about:

- supplied equipment, including buoyancy aids where relevant;
- briefing and in-water supervision;
- calm/sheltered conditions or beginner-site suitability;
- swimming, mobility, medical, age and weather requirements;
- pickup from the user's accommodation and the cancellation/rescheduling policy.

Position a first attempt as a low-pressure, brief supported experience. A novice should not feel obliged to complete the whole excursion or stay in the water after becoming uncomfortable.

## Google Maps short-link fallback

When a user supplies a `maps.app.goo.gl` link and managed web search is unavailable, resolve it from the HTTP redirect rather than guessing the venue/address:

```bash
curl -sI 'https://maps.app.goo.gl/<id>' | grep -i '^location:'
```

The redirect location frequently contains a `q=` parameter with the named place and full address. Keep the original short link in the resulting note for mobile use; use the expanded redirect only to verify the displayed details. Training-data addresses must be labelled unverified until this or another live source confirms them.

## Accommodation-first itinerary design

For a short, resort-first stay, use a deliberately sparse pattern: arrival/reset day, one weather-dependent signature activity, one cultural/food/nature outing, a flexible final full day, and a protected departure. Recommend a rental car only when the user actually wants the road journey or multiple independent stops; otherwise compare it against door-to-door drivers and operator pickups.

Holiday arrivals require a special check: festive menus, surcharges, venue/tour opening hours and airport-transfer availability are not normal-week assumptions. Mark them `to verify` until a live source confirms them.

## Durable note handling

Before creating a new planning file, search the known canonical notes/vault for earlier trip research and update/link it rather than creating an isolated duplicate. In a shared, sync-hosted vault, follow the established ownership convention for newly created notes (e.g. readable file/directory modes) and verify after writing.

## Deliverable standard

Return a short decision-ready summary containing:

- the recommended property and exact room/rate assumption;
- a compact alternatives table;
- a five-night low-pressure itinerary;
- key booking order and risks; and
- the saved-note path, if the user requested persistent documentation.

## Reference material

- Road-trip posts go to Telegram topic "Road trips": delivery target `telegram:-1001155335275:16749`.
- Sathya enjoys thrift stores, used book stores, specialty coffee (proper 5-6oz cappuccino, not Starbucks) and exploring indie/local neighbourhoods.

- `references/sydney-day-drives.md`: Sydney day drives already done or covered, plus less-obvious candidates with verified stops.

- `references/fiji-marriott-christmas-2026.md` — an example of pricing, transfer trade-offs and documentation conventions for a Christmas Fiji comparison.
