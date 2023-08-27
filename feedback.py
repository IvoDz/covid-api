import datetime
"""
class Feedback
Adjusts MongoDB schema to python 
Initialize with POST parameters to convert to dict,
later on access with get_feedback for convenient inserting to DB 
"""
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