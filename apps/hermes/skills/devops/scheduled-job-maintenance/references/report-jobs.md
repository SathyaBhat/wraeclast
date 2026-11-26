# Report jobs: summary plus detail

## What the user wants

A short summary as a normal message in the main channel, with the detailed report as a **threaded reply under that message**, so both show up in the channel. A separate flat post does not meet this, and neither does a standalone thread, which the user can't see from the channel.

## Pattern: one job plus a posting tool (Discord)

A cron delivery cannot open a thread anchored to its own message, so the posting happens through a tool:

1. Use the local plugin `super-report-discord` (`/opt/data/plugins/super-report-discord`). It registers the tool `post_super_report(summary, details, thread_name)` in toolset `super_report`. The tool posts `summary` to the hard-coded channel, starts a PUBLIC thread from that message (`POST /channels/{ch}/messages/{msg}/threads`), and posts `details` in ≤1900-char chunks. It reads the bot token through `tools.discord_tool._get_bot_token()` inside the gateway, so the token never enters the model context or a script environment. To reuse the tool for another report or channel, copy the plugin and change `CHANNEL_ID`. Don't make the channel a free-form argument.
2. Use a single job with `enabled_toolsets: ["web", "super_report"]` and `deliver: local` (the tool posts, so a normal delivery would double-post). Set `failure_deliver: discord:<channel_id>` so failures still reach the user.
3. The prompt researches once and writes both texts from the same figures. It calls the tool exactly once, and on success the final response is the summary plus `Posted: message <id>, thread <id>`. On failure it retries once, then starts with `[CRON_FAILURE]` and includes both texts so nothing is lost.
4. Length limits: summary ≤120 words in the fixed labelled-line shape ending "Details in the thread below."; details ≤500 words, `n/a` for missing figures, ≤5 links. The model tends to overshoot word caps by about 10%, so set the cap below the real target.
5. Verify the first run: the tool result must show `success: true` with both a `message_id` and a `thread_id`, and the user must confirm they can see the thread under the message.

## Discord threading pitfalls

- Don't use `attach_to_session: true` for a Discord channel report. The scheduler's `create_handoff_thread` calls `create_thread` without a type, and discord.py then defaults to a PRIVATE thread. The post becomes invisible from the channel, while `delivery_outcome` still says `delivered`.
- A `delivered` outcome only proves the API accepted the message. Confirm that the user can see the post where they expect it before calling a threading change done.
- `deliver: discord:<channel_id>:<thread_id>` posts into a fixed, existing thread. Without the thread segment, delivery lands flat in the main channel.
