---
name: grocery-board
description: Use when managing household groceries or shopping lists.
---
# Household groceries

Trello Anavrin is the only canonical live grocery inventory: https://trello.com/b/R6QbjglY/anavrin (short link `R6QbjglY`).
Board ARI: `ari:cloud:trello::board/workspace/62212dc095930234cdffe885/6a9d4104e1f512635a8cbe5d`.

The user adopted the dashboard grocery prompt at:
https://github.com/SathyaBhat/photo-frame-dashboard/blob/6af4dc1df7533eff83c74e6f4ae47a6dc2ea3b72/docs/hermes-trello-prompt.md
These rules supersede the old four-list workflow. The family wall frame also edits cards and labels. Both Sathya and Jo can update inventory. Read the live board afresh before every report or action; do not rely on earlier reads.

## Lists and access
- Match active lists by the words `To Buy` and `Stocked`, ignoring leading emoji. Discover the live lists rather than assuming old IDs remain valid.
- `🛒 To Buy`: all purchasing needs, including low stock and shop-specific one-offs.
- `✅ Stocked`: items in the house.
- Old `Running Low` and `Need to Stock` lists are archived: never use or restore them.
- Never create another list.
- Never read Recipes, write to it, or move cards into or out of it. Leave unrelated lists untouched.
- Load deferred Trello schemas before use. Read To Buy and Stocked by list, not by a board-wide card read that would include Recipes. Paginate fully and check declared totals.

## Labels
Use exact case and spacing. Never create labels outside these conventions.
- Every card gets exactly one category: `Fruits & Veggies`, `Bakery`, `Dairy & Refrigerated`, `Meat & Seafood`, `Pantry`, `Snacks`, `Spices & Seasoning`, `Household`.
- Drinks, cordial and soda mixes belong in Pantry.
- Frame-created cards may lack a category; whenever touching one, add the closest of the eight. Mention guessed categories in the reply.
- `Low` is optional and means running low or nearly out.
- Canonical `Usual` means regularly purchased and is independent of list and Low. Recognise `Usuals` in any case too. Apply the existing board label, whichever variant exists; create `Usual` only if neither exists. Preserve it on list moves and Low changes.
- Store is optional, at most one: `Store: <name>`. Apply only when the user names a specific shop; reuse the matching label. Creating a store label is allowed only when the named shop has none yet. Do not infer a store from prior shopping habits.
- Filter shopping reports by live Trello store labels only (case-insensitive store-name matching). For 'exclude Costco', omit only cards labelled `Store: CostCo`/`Store: Costco`; retain unlabelled cards. Never infer exclusions from Costco favourites, historical notes, or remembered shopping habits.

## Cards
- One card per generic item. Match case-insensitively and account for existing size/quantity names (e.g. 'milk' can match 'Milk 2L'). Match on the normalized generic name (see below), so brand/variety differences never create a second card.
- Normalize every item name before matching, adding, or renaming: use the generic item only.
  - Strip brand names: `Lindt Dark Chocolate`, `Cadbury Dark Chocolate` -> `Dark Chocolate`.
  - Collapse varieties/cultivars to the generic produce: `Kensington Pride Mango`, `R2E2 Mangoes` -> `Mangoes`; `Pink Lady Apples` -> `Apples`; `Cherry Tomatoes` stays only if the user clearly treats it as a different item from `Tomatoes` -- otherwise ask or keep generic.
  - Strip weight, size, pack count, quantity, percentages (e.g. 85%), and quality/marketing wording (Finest, I’m Perfect, Organic, Premium).
  - Use plural/singular consistently with the existing card (prefer the existing card's form); do not create `Mango` alongside `Mangoes`.
  - Keep distinctions only when they are genuinely different products in use (e.g. Low Carb Wraps versus Spinach Wraps, Spreadable Butter versus Butter, Dark versus Milk Chocolate). A brand or cultivar alone is never such a distinction.
- Before creating any card, search both To Buy and Stocked for the normalized name AND close variants (brand-prefixed, varietal, plural/singular). If a brand/variety-named card already exists, rename it in place to the generic name and reuse it instead of creating a new one. If two existing cards collapse to the same generic item, report them as duplicates and ask before merging/archiving (never delete).
- Use item-only card names: e.g. `Spreadable Butter`, `Mandarins`, `Dark Chocolate`, `Mangoes`. Do not append receipt quantities or weights. Apply this convention to both To Buy and Stocked; rename in place without moving.
- Descriptions are only free-text notes supplied by the user. Do not write category/store metadata or `Category:` lines there: the frame reads labels.
- Never delete a card. Archive a mistaken addition when asked to remove it.

## Operations
Always read both To Buy and Stocked first and reuse an existing card.

### Adding / need an item
- Already To Buy: do not duplicate. Keep the item-only name; do not append a supplied quantity.
- In Stocked: always move back to To Buy, preserving Usual, category and store labels. Add Low only if the user says low/running out.
- No matching card in either list: create in To Buy with exactly one category. Add Low when low/nearly out; add the Store label when a specific shop is named.
- Choose the closest category if unsure and state that assumption briefly. Non-food items (hardware, DIY, cleaning, toiletries) go in Household.
- A user-supplied spec that isn't a quantity (grit, size type, model) goes in the description as a note, and the card name stays generic: e.g. `Sandpaper` with description `220 grit`.

### Bought / got an item
- Move the matching card from To Buy to Stocked and remove Low; preserve other labels.
- If no matching card is in To Buy, say so. Do not invent one for a plain 'bought' request. If the user explicitly asks to add receipt items to Stocked, reuse matches in either list and create absent purchased items directly in Stocked with exactly one category. Always use item-only names, including for receipts: never add weights, sizes, quantities, pack counts, or quality/marketing wording. Clean these from an existing matched card when updating it.

### Running out / out / low
- In Stocked: move to To Buy and add Low.
- Already To Buy: add Low without duplicating.
- Absent: create in To Buy with category and Low, following adding rules.

### Usuals
- 'Make eggs a usual', 'we always buy eggs': add the existing Usual/Usuals label wherever the card is; do not move it.
- Absent: create in Stocked with category and Usual.
- 'Not a usual anymore': remove Usual without moving or archiving the card.

## Verification and replies
- Verify every external write by reading back the exact target card/list before claiming success.
- Keep replies short, naming what changed and any guessed category.
- For bulk work compare names/status/labels programmatically, not with mental totals.
- Page Stocked with `limit: 25`, not 50. A 50-card page exceeds the inline result size, spills to a file, and the spilled copy carries an abbreviated cursor containing `...`; 25-card pages stay inline with a usable full cursor.
- If a cursor is still abbreviated, rebuild it deterministically rather than guessing: it is base64 of compact JSON `{"position":<last card position>,"objectId":"<last card objectId>"}` from the last card of that page (`base64.b64encode(json.dumps({...}, separators=(',',':')).encode())`). Print the result in short chunks, because long base64 strings in tool output get abbreviated too. Deduplicate overlapping reads and continue until `hasNextPage` is false; never treat the first page as the complete inventory.
- Keep truncated receipt product names visibly unspecified rather than guessing a seasoning/flavour or merging them with a particular existing variant. (Brand and cultivar names are not flavours: still normalize those to the generic item.)
- Scan receipts with vision tools. Exclude discount/redemption lines and explicitly excluded products. Do not treat fresh sweet potato as frozen fries, or chicken thighs as curry-cut chicken without confirmation. Apply the bought rules rather than inventing absent cards.

## Other references
- Obsidian `Lists/Grocery Kanban.md` is a historical migration snapshot; never maintain a second live inventory. Costco favourites remain in Obsidian `Shopping/Costco Awesome Food List.md`.
- Asian shopping photo: `/opt/data/lists/asian-shopping-refs/haidilao-spicy-cumin-bbq-seasoning.jpg`, Haidilao Spicy Cumin BBQ Seasoning 40g from Blacktown Tong Li. Show it when asked for Asian shopping. Its Trello card is https://trello.com/c/grf8ZQYV. The image remains local; no Trello image upload has been performed.
- Live household inventory is the Trello Anavrin board (https://trello.com/b/R6QbjglY/anavrin). The Obsidian Grocery Kanban is a historical snapshot; Costco favourites and Seattle lists stay in Obsidian.
- Stores: Costco (bulk: spinach wraps, spicy peanuts), Coles (Kings Langley and Stanhope Gardens, regular groceries), Blacktown Tong Li (Asian groceries).
- Asian shopping reference photos are in /opt/data/lists/asian-shopping-refs/. Show them when asked about Asian shopping. Current item: haidilao-spicy-cumin-bbq-seasoning.jpg (Haidilao Spicy Cumin BBQ Seasoning 40g, Blacktown Tong Li).
- If category names or conventions change in the dashboard, keep these rules aligned with the source prompt and `CATEGORIES` in `dashboard/server/trello-map.js`; do not change dashboard code without user authorization.
