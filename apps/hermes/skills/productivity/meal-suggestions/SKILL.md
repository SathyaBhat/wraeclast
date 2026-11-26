---
name: meal-suggestions
description: Use for meal ideas or plans. Pick from RecipeTin Eats.
---

# Meal suggestions

Sathya's preferred recipe source is RecipeTin Eats (Nagi Maehashi, Sydney-based, so ingredients suit Australian shops). Use it whenever Sathya asks for food, dinner, recipe, or meal-plan suggestions.

## Workflow
1. Check the RecipeTin Eats category pages first, in this order of preference:
   - Quick & easy: https://www.recipetineats.com/category/quick-and-easy/
   - One pot: https://www.recipetineats.com/category/one-pot-recipes/
   - Home page (fallback / seasonal picks): https://www.recipetineats.com/
2. Fetch with curl, not web_extract. web_extract returns only the nav and pagination, with no recipe list. This command gives title | URL pairs:
   `curl -s -A "Mozilla/5.0" "https://www.recipetineats.com/category/quick-and-easy/" | grep -oE '<a[^>]+class="entry-title-link"[^>]*href="[^"]+"[^>]*>[^<]+' | sed -E 's/.*href="([^"]+)".*>(.*)/\2 | \1/'`
   Page 2 onward is at `.../page/N/`. Skip non-dinner items (sides, sauces, desserts).
3. Pick the suggestion(s) from those pages, and link each recipe's own URL. Prefer recipes that appear in both categories.
4. For meal plans, use mostly quick & easy and one-pot dishes, and vary the proteins and cuisines.
5. Optionally, cross-check against the Trello Anavrin grocery board (grocery-board skill) to use stocked items or add missing ingredients, but only if asked or clearly useful.

## Pitfalls
- Don't invent recipe names or URLs. Only suggest recipes you actually saw on the fetched pages.
- Fall back to general suggestions only if the site is unreachable, and say so.
