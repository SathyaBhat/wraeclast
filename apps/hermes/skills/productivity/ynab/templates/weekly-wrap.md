# Weekly Financial Wrap — Output Format & Category Emoji Map

## Output format
```
📊 Weekly Financial Wrap — DD Mon to DD Mon YYYY

💰 Total Spent: $X,XXX.XX

🏆 Top N Spending Categories
• [emoji] [Category]: Last Week Spend: $X.XX  Balance: $Y.YY [🚨 if balance < 0]
(sorted by spend, highest first)
```

## Category emoji map (Australia budget)
| Category name pattern       | Emoji | Display name              |
|-----------------------------|-------|---------------------------|
| fitness                     | 🧘    | Fitness                   |
| groceries / grocery         | 🍌    | Groceries                 |
| dining                      | 🍽️   | Dining Out                |
| breakfast / snacks          | ☕    | Breakfast & Snacks        |
| opal / transport            | 🚆    | Transport (Opal/Office)   |
| home decor / others         | 🛒    | Home Decor & Others       |
| jo's office / office food   | 🍱    | Jo's Office Food          |
| charg (EV)                  | ⚡    | EV Charging               |
| sathya / fun money          | 🎮    | Sathya's Fun Money        |
| clothing / footwear         | 👕    | Clothing & Footwear       |
| fuel / petrol               | ⛽    | Fuel                      |
| mortgage                    | 🏡    | Mortgage                  |
| taxi / uber / rideshare     | 🚕    | Transport (Rideshare)     |
| liquor / alcohol / beer/wine| 🍻    | Liquor                    |
| (fallback)                  | 💸    | (raw category name)       |

## Processing logic (Python sketch)
```python
from collections import defaultdict

cat_spend = defaultdict(float)
cat_name_map = {}

for t in transactions:
    if t.get('deleted') or t.get('transfer_account_id'):
        continue
    subtxns = t.get('subtransactions', [])
    entries = subtxns if subtxns else [t]
    for entry in entries:
        if entry.get('deleted'):
            continue
        cat_id = entry.get('category_id')
        cat_name = entry.get('category_name', '')
        if not cat_id or not cat_name:
            continue
        if cat_name.startswith('Inflow') or cat_name == 'Split':
            continue
        amount = entry.get('amount_currency', 0)
        if amount < 0:
            cat_spend[cat_id] += abs(amount)
            cat_name_map[cat_id] = cat_name

# Get balance per category from get_month() response
# month_data['categories'] → list of {id, balance_currency, budgeted_currency, ...}
categories_map = {c['id']: c for c in month_data['categories']}

# Over-budget: balance_currency < 0
```

## Notes
- **Skip** `category_name == "Split"` on the parent — always use `subtransactions` for the breakdown.
- **Skip** `transfer_account_id` set — these are account transfers, not spending.
- `get_month(month="YYYY-MM-01")` returns 187 categories for the Australia budget with full balance/goal data.
