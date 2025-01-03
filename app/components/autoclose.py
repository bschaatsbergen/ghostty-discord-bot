import datetime as dt
from collections.abc import Sequence
from typing import cast

import discord
from discord.ext import tasks

from app.setup import bot, config


@tasks.loop(hours=1)
async def autoclose_solved_posts() -> None:
    closed_posts: list[discord.Thread] = []
    failures: list[discord.Thread] = []

    help_channel = cast(discord.ForumChannel, bot.get_channel(config.HELP_CHANNEL_ID))
    open_posts = len(help_channel.threads)
    for post in help_channel.threads:
        if post.archived or not (
            _has_tag(post, "solved") or _has_tag(post, "moved to github")
        ):
            continue
        if post.last_message_id is None:
            failures.append(post)
            continue
        one_day_ago = dt.datetime.now(tz=dt.UTC) - dt.timedelta(hours=24)
        if discord.utils.snowflake_time(post.last_message_id) < one_day_ago:
            await post.edit(archived=True)
            closed_posts.append(post)

    log_channel = cast(discord.TextChannel, bot.get_channel(config.LOG_CHANNEL_ID))
    msg = f"Scanned {open_posts} open posts in {help_channel.mention}.\n"
    if closed_posts:
        msg += f"Automatically closed {_post_list(closed_posts)}"
    if failures:
        msg += f"Failed to check {_post_list(failures)}"
    await log_channel.send(msg)


def _has_tag(post: discord.Thread, substring: str) -> bool:
    return any(substring in tag.name.casefold() for tag in post.applied_tags)


def _post_list(posts: Sequence[discord.Thread]) -> str:
    return f"{len(posts)} solved posts:\n" + "\n".join(
        f"* {post.mention}" for post in posts
    )
