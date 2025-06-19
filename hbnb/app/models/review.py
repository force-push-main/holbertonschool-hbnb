from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text=None, rating=None, place_id=None, user_id=None):
        super().__init__()

        self.text = text
        self.rating = rating
        self.place = place_id
        self.user = user_id

    # @property
    # def place(self):
    #     return self.place

    # @place.setter
    # def place(self, obj):
    #     if not issubclass(obj, Place):
    #         raise TypeError("Property must be a property object")
    #     if not InMemoryRepository.get(obj.id):
    #         raise NameError("Property not found")

# review object is attached to a place object by place id, review can only have one place
# should check whether place object exists before attaching review to place

    # @property
    # def user(self):
    #     return self.user
    
    # @user.setter
    # def user(self, obj):
    #     if not issubclass(obj, User):
    #         raise TypeError("User must be a user object")
    #     if not InMemoryRepository.get(obj.id):
    #         raise NameError("User not found")
