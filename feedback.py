import datetime

class Feedback:
    def __init__(self, user, comm, favorite):
        self.feedback = {
            "user": user,
            "timestamp": datetime.datetime.utcnow()
        }
        
        if comm is not None:
            self.feedback["comment"] = comm
        
        if favorite is not None:
            self.feedback["favorite"] = favorite

    def get_feedback(self):
        return self.feedback