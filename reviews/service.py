import streamlit as st

from reviews.repository import ReviewsRepository


@st.cache_data(ttl=120)  # Cache por 2 minutos
def _get_reviews_cached():
    repository = ReviewsRepository()
    return repository.get_reviews()


class ReviewsService:

    def __init__(self):
        self.review_repository = ReviewsRepository()

    def get_reviews(self):
        return _get_reviews_cached()

    def create_review(self, movie_id, star, comment):
        review = dict(
            movie=movie_id,
            stars=star,
            comment=comment,
        )
        new_review = self.review_repository.create_review(review)
        _get_reviews_cached.clear()

        return new_review

    def refresh_reviews(self):
        _get_reviews_cached.clear()
        return self.get_reviews()
