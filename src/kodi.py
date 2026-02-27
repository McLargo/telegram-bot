"""Kodi client to interact with the Kodi media center."""

from typing import List

import requests

from src.models import Movie, TVShow, TVShowSeason


class KodiClient:
    """Client to interact with the Kodi media center using JSON-RPC API."""

    def __init__(self, kodi_config, logger):
        """Initialize the Kodi class with the given configuration."""
        self.config = kodi_config
        self.logger = logger
        self.url = f"http://{self.config.ip}:{self.config.port}/jsonrpc"
        self.auth = (
            (self.config.username, self.config.password)
            if self.config.username and self.config.password
            else None
        )

    def _query_kodi(self, method, params=None):
        """Internal method to send a JSON-RPC request to Kodi."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {},
        }
        try:
            return requests.post(
                self.url,
                json=payload,
                auth=self.auth,
                timeout=5,
            ).json()
        except requests.RequestException as e:
            self.logger.error("Error querying Kodi: %s", e)
            return {}
        except requests.ConnectionError as e:
            self.logger.error("Error connecting to Kodi: %s", e)
            return {}

    def refresh_library(self) -> None:
        """Refresh the Kodi library."""
        self._query_kodi("VideoLibrary.Scan")

    def get_movies(self) -> List[Movie]:
        """Get the list of movies from Kodi."""
        params = {
            "properties": ["title", "year"],
        }
        response = self._query_kodi("VideoLibrary.GetMovies", params)
        movies = response.get("result", {}).get("movies", [])
        list_of_movies = []
        for movie in movies:
            new_movie = Movie(
                title=movie.get("title", "Unknown"),
                year=movie.get("year", "N/A"),
            )
            list_of_movies.append(new_movie)
            self.logger.debug("Retrieved movie: %s", new_movie.__dict__)
        return list_of_movies

    def get_tv_shows(self) -> List[TVShow]:
        """Get the list of TV shows, seasons and episodes count from Kodi."""
        params = {
            "properties": ["title", "year"],
        }
        response = self._query_kodi("VideoLibrary.GetTVShows", params)
        tv_shows = response.get("result", {}).get("tvshows", [])
        list_of_tv_shows = []

        for show in tv_shows:
            new_show = TVShow(
                title=show.get("title", "Unknown"),
                year=show.get("year", "N/A"),
            )
            params = {
                "tvshowid": int(show["tvshowid"]),
                "properties": ["season", "episode"],
            }
            data = self._query_kodi("VideoLibrary.GetSeasons", params)
            seasons = data.get("result", {}).get("seasons", [])

            for season in seasons:
                new_season = TVShowSeason(
                    season_number=season.get("season", "Unknown"),
                    episode_count=season.get("episode", "N/A"),
                )
                new_show.seasons.append(new_season)
            self.logger.debug("Retrieved TV show: %s", new_show.__dict__)
            list_of_tv_shows.append(new_show)

        return list_of_tv_shows
