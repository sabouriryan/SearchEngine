class Posting:
    def __init__(self, token, doc_id, tf_idf) -> None:
        self.token = token
        self.doc_id = doc_id
        self.tf_idf = tf_idf

    
    def convert_to_tuple(self)->tuple:
        return (self.token, self.doc_id, self.tf_idf)

