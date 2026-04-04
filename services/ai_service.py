from models import Follow
from extensions import db
from collections import Counter

def recommend_users(user_id):
   # Get users I follow
   following = db.session.query(Follow.following_id)\
      .filter(Follow.follower_id == user_id).all()

   following_ids = [f[0] for f in following]

   # Get friends of friends
   second_degree = db.session.query(Follow.following_id)\
      .filter(Follow.follower_id.in_(following_ids)).all()

   second_ids = [s[0] for s in second_degree]

   # count frequency
   recommendations = Counter(second_ids)

   # Remove followed + self
   for f in following_ids:
      recommendations.pop(f,None)

   recommendations.pop(user_id,None)

   return [user for user, _ in recommendations.most_common(5)]

