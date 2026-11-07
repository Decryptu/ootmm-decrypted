"""Read-only timing evidence for the disposable gameplay observer."""
import time


class MailboxTiming:
    def __init__(self, clock=time.monotonic):
        self.clock = clock
        self.started = clock()
        self.history = []
        self.recoveries = []
        self.lost_at = None
        self.previous_mailbox = None
        self.poll_count = 0
        self.max_poll_seconds = 0.0

    def observe(self, mailbox, received_index, poll_started):
        now = self.clock()
        self.poll_count += 1
        self.max_poll_seconds = max(self.max_poll_seconds, now - poll_started)
        if self.history and self.history[-1]["mailbox"] == mailbox:
            return None
        event = {"mailbox": mailbox, "received_index": received_index,
                 "elapsed_seconds": now - self.started}
        self.history.append(event)
        if mailbox is None:
            if self.previous_mailbox is not None and self.lost_at is None:
                self.lost_at = now
        else:
            if self.lost_at is not None:
                self.recoveries.append({"from_mailbox": self.previous_mailbox, "to_mailbox": mailbox,
                                        "seconds": now - self.lost_at})
            self.previous_mailbox = mailbox
            self.lost_at = None
        return event

    def report(self):
        return {"poll_count": self.poll_count, "max_poll_seconds": self.max_poll_seconds,
                "recoveries": list(self.recoveries),
                "pending_recovery_seconds": None if self.lost_at is None else self.clock() - self.lost_at}
