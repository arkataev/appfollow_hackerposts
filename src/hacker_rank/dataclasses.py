from datetime import datetime
from typing import NamedTuple


class HackerPost(NamedTuple):
    id: int                     # The item's unique id
    title: str                  # The title of the story, poll or job. HTML.
    time: int                   # Unix time when post was created
    url: str                    # The URL of the story.
    saved_at: datetime = None   # When post was saved to storage
