from typing import List

import click

from repository import LocalMarkingRepo


class MarkingService:

    def __init__(self, local_marking_repo: LocalMarkingRepo) -> None:
        super().__init__()
        self.local_marking_repo = local_marking_repo

    def mark_seen(self, ids: List[int]):
        print('Marking ', end='')
        for mid in ids:
            print(mid, end=' ')
            self.local_marking_repo.mark_seen(mid)
        print('as seen...')

    def un_mark_seen(self, ids: List[int]):
        db_ids = []

        click.echo('Un-marking ', nl=False)

        for mid in ids:
            click.echo(f"{mid} ", nl=False)
            db_ids += self.local_marking_repo.un_mark_seen(mid)

        click.echo('as seen...')
        click.echo(f"Removed {len(db_ids)} records.")
