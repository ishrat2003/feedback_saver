from .base import Base

class Story(Base):

    def __init__(self):
        super().__init__()
        self.tableName = 'story'
        self.keyAttributes = ['story_link', 'user_code']
        self.attributes = self.commonArrtibutes + [
            'story_source',
            'story_date',
            'story_link', 
            'story_title',
            'who',
            'what',
            'where_location',
            'why', 
            'when_happened'
        ]
        return
    
    def _checkError(self, attribute, data):
        if attribute == 'where_location':
            self.errors.append('Where is required.')
        elif attribute == 'when_happened':
            self.errors.append('When is required.')
        else:
            self.errors.append(attribute[0].upper() + attribute[1:] + ' is required.')

        return