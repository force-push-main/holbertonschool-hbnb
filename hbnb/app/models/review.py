from app.models.base import BaseModel

class Review(BaseModel):
    def __init__(self, text=None, rating=None, place=None, user=None):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    # @property
    # def text(self):
    #     return self.text
    
    # @text.setter
    # def text(self, value):
    #     if not value:
    #         raise ValueError("Review must contain text")
    #     if type(value) != str:
    #         raise TypeError("Review must be a string")
    #     self.text = value

    # @property
    # def rating(self):
    #     return self.rating
    
    # @rating.setter
    # def rating(self, value):
    #     if type(value) != int:
    #         raise TypeError("Rating must be an int")
    #     if value < 1 or value > 5:
    #         raise ValueError("Rating must be a value between 1 and 5")
    #     self.rating = value

    # @property
    # def place(self):
    #     return self.place

    # @place.setter
    # def place(self, obj):
    #     if not issubclass(obj, Place):
    #         raise TypeError("Property must be a property object")
    #     if not InMemoryRepository.get(obj.id):
    #         raise NameError("Property not found")

    # @property
    # def user(self):
    #     return self.user
    
    # @user.setter
    # def user(self, obj):
    #     if not issubclass(obj, User):
    #         raise TypeError("User must be a user object")
    #     if not InMemoryRepository.get(obj.id):
    #         raise NameError("User not found")
