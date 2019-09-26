from typing import List

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
