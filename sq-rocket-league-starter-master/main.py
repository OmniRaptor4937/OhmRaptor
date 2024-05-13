# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits



class Bot(GoslingAgent):
  # This function runs every in-game tick (every time the game updates anything)
  def run(self):
      # set_intent tells the bot what it's trying to do

      opponent1 = self.foes[0]
      opponent1_location_x = opponent1.location.x
      opponent1_location_y = opponent1.location.y
      opponent1_location_z = opponent1.location.z

      ball_x = self.ball.location.x
      ball_y = self.ball.location.y

      my_x = self.me.location.x
      my_y = self.me.location.y
      my_z = self.me.location.z

      friend_goal_x = self.friend_goal.location.x
      friend_goal_y = self.friend_goal.location.y

      available_small_boosts = [boost for boost in self.boosts if boost.small and boost.active]
      

      #Don't fully know if I want to use these like this
      # defend_goal =  {'friend_goal': (self.friend_goal.right_post, self.friend_goal.left_post)}
      # attack_goal = {'foe_goal': (self.foe_goal.left_post, self.foe_goal.right_post)}

      targets = {'foe_goal': (self.foe_goal.left_post, self.foe_goal.right_post), 
                  'friend_goal': (self.friend_goal.right_post, self.friend_goal.left_post)}
      
      
      closest_large_boost = self.get_closest_large_boost()
      closest_small_boost = self.get_closest_small_boost()
      closest_goal_boost = self.get_closest_goal_boost()
      # boost_or_ball = self.get_boost_or_ball()

      hits = find_hits(self, targets)


      if self.get_intent() is not None:
          return
      
      if self.kickoff_flag == True:
          self.set_intent(kickoff())
          # print('I kicked the ball!')
          return
      


      # Situation of What to do if the ball is 50/50 to the side of kickoff.
      if (self.me.location.y - self.ball.location.y) <= 500 and (opponent1.location.y - self.ball.location.y) > 500:
          self.set_intent(goto(closest_small_boost.location))
          if len(hits['foe_goal']) > 0:
            self.set_intent(hits['foe_goal'][0])
          return
    
      
      # Ball on our side logic/ NOTe MAKE SURE TO ADD THE CLOSER TO OUR GOAL IN
      if self.me.location.y > self.ball.location.y and abs(self.ball.location.y) > 2560 and (self.ball.location - self.friend_goal.location).magnitude() < (self.ball.location - self.foe_goal.location).magnitude():
          self.set_intent(goto(closest_goal_boost.location))
          if len(hits['friend_goal']) > 0:
              self.set_intent(hits['friend_goal'][0])
          return
          
      # Ball on their side.
      if self.me.location.y < self.ball.location.y and abs(self.ball.location.y) > 2560 and (self.ball.location - self.friend_goal.location).magnitude() > (self.ball.location - self.foe_goal.location).magnitude():
        self.set_intent(goto(closest_small_boost))
          if len(hits['foe_goal']) > 0:
            self.set_intent(hits['foe_goal'][0])
        return

      


                              

      if closest_goal_boost is not None:
          self.set_intent(goto(closest_goal_boost.location))
          return

      # if len(hits['foe_goal']) > 0:
      #     self.set_intent(hits['foe_goal'][0])
      #     return
      

      self.clear_intent()
        

        
        
        
