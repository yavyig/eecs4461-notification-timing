"""Project-specific notification agents, adapted from Mesa's agent/model pattern."""

from mesa import Agent


class NotificationAgent(Agent):
    """A notification record, not a simulated person or attention state."""

    def __init__(self, model, notification_id, arrival_minute):
        super().__init__(model)
        self.notification_id = notification_id
        self.arrival_minute = arrival_minute
        self.state = "scheduled"
        self.presentation_minute = None
        self.presentation_delay = None
        self.release_count = 0

    def step(self):
        if self.state == "scheduled" and self.arrival_minute == self.model.minute:
            self.state = "pending"
            self.model.pending.append(self)

    def present(self):
        if self.state != "pending":
            raise RuntimeError("Only a pending notification may be presented")
        self.presentation_minute = self.model.minute
        self.presentation_delay = self.presentation_minute - self.arrival_minute
        self.release_count += 1
        self.state = "presented"
