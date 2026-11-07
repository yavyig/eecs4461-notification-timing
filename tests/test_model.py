"""Checks of timing boundaries, conservation, and the controlled comparison."""

import unittest

from src.project_model.model import DISPERSED_ARRIVALS, NotificationModel


class NotificationTimingTests(unittest.TestCase):
    def test_exact_boundary_and_simultaneous_arrivals(self):
        model = NotificationModel("batch", arrivals=(0, 9, 10, 10, 11, 60)).run()
        self.assertEqual([a.presentation_minute for a in model.notifications],
                         [0, 10, 10, 10, 20, 60])
        self.assertEqual(model.episode_count, 4)

    def test_horizon_flush_and_no_empty_episodes(self):
        model = NotificationModel("batch", arrivals=(58,), batch_interval=13).run()
        self.assertEqual(model.notifications[0].presentation_minute, 60)
        self.assertEqual(model.episode_count, 1)
        self.assertEqual(NotificationModel("batch", arrivals=()).run().episode_count, 0)

    def test_immediate_simultaneous_notifications_share_one_episode(self):
        model = NotificationModel("immediate", arrivals=(3, 3, 8)).run()
        self.assertEqual(model.episode_count, 2)
        self.assertTrue(all(a.presentation_delay == 0 for a in model.notifications))

    def test_conservation_and_no_early_or_duplicate_release(self):
        for mode in ("immediate", "batch"):
            model = NotificationModel(mode).run()
            self.assertEqual(len(model.notifications), 12)
            self.assertFalse(model.pending)
            for row in model.notification_trace():
                self.assertEqual(row["release_count"], 1)
                self.assertEqual(row["final_state"], "presented")
                self.assertGreaterEqual(row["presentation_delay_minutes"], 0)
            states = model.datacollector.get_model_vars_dataframe()
            self.assertTrue(((states.scheduled_count + states.pending_count
                              + states.presented_count) == 12).all())
            self.assertEqual(len(states), 61)
            self.assertEqual(states.iloc[-1].minute, 60)

    def test_controlled_results_against_independent_arithmetic(self):
        baseline = NotificationModel("immediate").run()
        alternative = NotificationModel("batch").run()
        expected = [10 * ((a + 9) // 10) for a in DISPERSED_ARRIVALS]
        self.assertEqual([a.presentation_minute for a in alternative.notifications], expected)
        self.assertEqual(baseline.episode_count, 12)
        self.assertEqual(alternative.episode_count, 6)
        self.assertEqual(sum(a.presentation_delay for a in baseline.notifications), 0)
        self.assertEqual(sum(a.presentation_delay for a in alternative.notifications), 60)
        self.assertEqual(max(a.presentation_delay for a in alternative.notifications), 8)

    def test_invalid_arrival_rejected(self):
        with self.assertRaises(ValueError):
            NotificationModel(arrivals=(61,))


if __name__ == "__main__":
    unittest.main()
