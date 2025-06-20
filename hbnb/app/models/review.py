from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text=None, rating=None, place=None, user=None):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
