from datetime import date, timedelta
from app.services.progress_service import calculate_xp_gained, calculate_streak, compute_level


class TestCalculateXpGained:
    def test_correct_answers_give_10_each(self):
        answers = [
            type("A", (), {"was_correct": True})(),
            type("A", (), {"was_correct": True})(),
            type("A", (), {"was_correct": False})(),
        ]
        assert calculate_xp_gained(score=2, total=3, answers=answers) == 20

    def test_perfect_score_adds_50_bonus(self):
        answers = [type("A", (), {"was_correct": True})() for _ in range(3)]
        assert calculate_xp_gained(score=3, total=3, answers=answers) == 80  # 30 + 50

    def test_zero_correct_no_perfect_bonus(self):
        answers = [type("A", (), {"was_correct": False})() for _ in range(5)]
        assert calculate_xp_gained(score=0, total=5, answers=answers) == 0


class TestCalculateStreak:
    def test_first_play_sets_streak_to_1(self):
        today = date.today()
        assert calculate_streak(last_played=None, today=today, current_streak=0) == 1

    def test_consecutive_day_increments_streak(self):
        today = date.today()
        yesterday = today - timedelta(days=1)
        assert calculate_streak(last_played=yesterday, today=today, current_streak=5) == 6

    def test_same_day_keeps_streak(self):
        today = date.today()
        assert calculate_streak(last_played=today, today=today, current_streak=3) == 3

    def test_gap_resets_streak_to_1(self):
        today = date.today()
        two_days_ago = today - timedelta(days=2)
        assert calculate_streak(last_played=two_days_ago, today=today, current_streak=10) == 1


class TestComputeLevel:
    def test_zero_xp_is_level_1(self):
        assert compute_level(0) == 1

    def test_499_xp_is_level_1(self):
        assert compute_level(499) == 1

    def test_500_xp_is_level_2(self):
        assert compute_level(500) == 2

    def test_999_xp_is_level_2(self):
        assert compute_level(999) == 2

    def test_level_capped_at_10(self):
        assert compute_level(4500) == 10
        assert compute_level(99999) == 10
