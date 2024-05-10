# This file is for strategy

from util.objects import *
from util.routines import *
from util.tools import find_hits
from threading import Timer


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
        boost_or_ball = self.get_boost_or_ball()

        hits = find_hits(self, targets)


        if self.get_intent() is not None:
            return
        
        if self.kickoff_flag == True:
            self.set_intent(kickoff())
            # print('I kicked the ball!')
            return

        # Situation of What to do if the ball is 50/50 to the side of kickoff.
        if abs(self.me.location - self.ball.location).magnitude() <= 500 and abs(opponent1.location - self.ball.location).magnitude > 500:
            self.set_intent(goto(boost_or_ball.location))
            timer = Timer(.3)
            timer.start
            self.set_intent(hits['foe_goal'][0])
            return
        
        # Ball on our side logic
        # left_post_to_us = None
        # right_post_to_us = None
        # if (self.ball.location - self.friend_goal.location).magnitude() < (self.ball.location - self.foe_goal.location).magnitude():
        #     if (self.me.location - self.friend_goal.left_post).magnitude() < (self.me.location - self.friend_goal.right_post).magnitude() and left_post_to_us is None:
        #         self.set_intent(goto(self.friend_goal.left_post + 250))
        #         left_post_to_us = 1
        #         timer = Timer(.5)
        #         timer.start
        #         self.set_intent(hits['friend_goal'][0])
        #         timer.start
        #         print('go for ball')
        #         return
        #     if right_post_to_us is None:
        #         self.set_intent(goto(self.friend_goal.right_post+250))
        #         right_post_to_us = 1
        #         timer = Timer(.5)
        #         timer.start
        #         self.set_intent(hits['friend_goal'][0])
        #         timer.start
        #         return
            
        if (self.ball.location - self.friend_goal.location).magnitude() > (self.ball.location - self.foe_goal.location).magnitude():
            self.set_intent(goto(closest_large_boost))
            return

                                

        if self.me.boost <= 33 and closest_small_boost is not None:
            self.set_intent(goto(closest_small_boost.location))
            return

        if len(hits['foe_goal']) > 0:
            self.set_intent(hits['foe_goal'][0])
            return
        
        if len(hits['friend_goal']) > 0:
            self.set_intent(hits['friend_goal'][0])
            return
        # timer1 = Timer(2)
        # timer1.start
        self.clear_intent()
        

            

        
        
        
