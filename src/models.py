"""Models for my service."""


class Movie:
    """Class representing a movie."""

    def __init__(self, title, year):
        """Initialize the Movie class with the given title and year."""
        self.title = title
        self.year = year

    def __repr__(self):
        """Return a string representation of the Movie instance."""
        return f"Movie(title={self.title!r}, year={self.year!r})"


class TVShowSeason:
    """Class representing a season of a TV show."""

    def __init__(self, season_number, episode_count):
        """Initialize the TVShowSeason class.

        Args:
            season_number: The season number.
            episode_count: The number of episodes in the season.
        """
        self.season_number = season_number
        self.episode_count = episode_count

    def __repr__(self):
        """Return a string representation of the TVShowSeason instance."""
        return (
            f"Season(number={self.season_number}, "
            f"episodes={self.episode_count})"
        )


class TVShow:
    """Class representing a TV show."""

    def __init__(self, title, year):
        """Initialize the TVShow class with the given title and year."""
        self.title = title
        self.year = year
        self.seasons = []

    def __repr__(self):
        """Return a string representation of the TVShow instance."""
        return (
            f"TVShow(title={self.title!r}, year={self.year!r}, "
            f"seasons={self.seasons!r})"
        )
