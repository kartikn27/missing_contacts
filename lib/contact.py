class Contact(object):
    def __init__(self, attributes, relationships):
        self.attributes = attributes
        self.relationships = relationships

    def get_attributes(self):
        return self.attributes

    def get_relationships(self):
        return self.relationships

