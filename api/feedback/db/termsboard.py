from .base import Base

class Termsboard(Base):

    def __init__(self):
        super().__init__()
        self.tableName = 'termsboard'
        self.keyAttributes = ['story_term', 'user_code']
        self.attributes = self.keyAttributes + self.commonArrtibutes
        return
    
    def _checkError(self, attribute, data):
        self.errors.append(attribute[0].upper() + attribute[1:] + ' is required.')
        return