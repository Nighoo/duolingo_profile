"""Profile data models for Duolingo Profile integration."""

from typing import List, Optional, TypedDict


class CourseData(TypedDict, total=False):
    """Data model for a course in the Duolingo profile."""

    crowns: int


class CurrentStreak(TypedDict):
    """Data model for the current streak in the Duolingo profile."""

    endDate: str


class StreakData(TypedDict, total=False):
    """Data model for streak data in the Duolingo profile."""

    currentStreak: CurrentStreak


class ProfileData(TypedDict):
    """TypedDict for the Duolingo profile data response."""

    username: str
    streak: int
    totalXp: int
    courses: List[CourseData]
    streakData: StreakData
