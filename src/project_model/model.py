"""A selective, synthetic representation of notification delivery timing.

Structural starting point: Mesa v3.5.1 Boltzmann Wealth Model (see SOURCE.md).
Retained patterns: Model, agents, agent activation, and DataCollector.
Replaced: spatial movement, wealth transfer, and Gini with notification states,
a shared pending queue, a presentation rule, and timing/count outputs.
"""

from mesa import Model
from mesa.datacollection import DataCollector

from .agents import NotificationAgent

DISPERSED_ARRIVALS = (3, 8, 12, 17, 22, 28, 33, 38, 42, 47, 52, 58)


class NotificationModel(Model):
    def __init__(self, delivery_mode="immediate", arrivals=DISPERSED_ARRIVALS,
                 batch_interval=10, horizon=60):
        super().__init__(rng=0)
        if delivery_mode not in ("immediate", "batch"):
            raise ValueError("delivery_mode must be immediate or batch")
        if not isinstance(horizon, int) or horizon < 0:
            raise ValueError("horizon must be a nonnegative integer")
        if not isinstance(batch_interval, int) or batch_interval <= 0:
            raise ValueError("batch_interval must be a positive integer")
        if any(not isinstance(a, int) or not 0 <= a <= horizon for a in arrivals):
            raise ValueError("arrivals must be integer minutes within the horizon")
        self.delivery_mode = delivery_mode
        self.batch_interval = batch_interval
        self.horizon = horizon
        self.minute = -1
        self.pending = []
        self.release_log = []
        self.episode_count = 0
        self.notifications = [
            NotificationAgent(self, f"N{i:02d}", arrival)
            for i, arrival in enumerate(arrivals, start=1)
        ]
        self.datacollector = DataCollector(model_reporters={
            "minute": "minute",
            "scheduled_count": lambda m: sum(a.state == "scheduled" for a in m.agents),
            "pending_count": lambda m: len(m.pending),
            "presented_count": lambda m: sum(a.state == "presented" for a in m.agents),
            "cumulative_alert_episodes": "episode_count",
        })

    def step(self):
        if self.minute >= self.horizon:
            self.running = False
            return
        self.minute += 1
        # First admit all arrivals, then release. Boundary arrivals are eligible.
        self.agents.do("step")
        release_due = (self.delivery_mode == "immediate"
                       or self.minute % self.batch_interval == 0
                       or self.minute == self.horizon)
        if release_due and self.pending:
            episode_members = list(self.pending)
            for notification in episode_members:
                notification.present()
            self.release_log.append({
                "minute": self.minute,
                "notification_ids": [a.notification_id for a in episode_members],
            })
            self.episode_count += 1
            self.pending.clear()
        self.datacollector.collect(self)
        if self.minute == self.horizon:
            self.running = False

    def run(self):
        while self.running:
            self.step()
        return self

    def notification_trace(self):
        return [{"notification_id": a.notification_id,
                 "arrival_minute": a.arrival_minute,
                 "presentation_minute": a.presentation_minute,
                 "presentation_delay_minutes": a.presentation_delay,
                 "final_state": a.state,
                 "release_count": a.release_count}
                for a in self.notifications]
