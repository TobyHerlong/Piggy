from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 99
        self.RIGHT_DEFAULT = 99
        self.EXIT_HEADING = 0
        self.SAFE_DIST = 300
        self.MIDPOINT = 1400  # what servo command (1000-2000) is straight forward for your bot?
        self.load_defaults()
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "c": ("Calibrate", self.calibrate),
                "s": ("Stop", self.stop),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()

    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''

    def dance(self):
        """START DANCING"""
        #HIGHER - ORDER
        for x in range(1):
            self.shuffle()
            self.wiggle()
            self.crazy()
            self.itdances()
            
    
    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 300):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the  number of obstacles it see"""
        found_something = False # trigger
        trigger_distance = 125
        count = 0
        starting_position = self.get_heading()
        time.sleep(1)
        self.right(primary=70, counter=-70)
        while self.get_heading() != starting_position:
            if self.read_distance() < trigger_distance and not found_something:
                found_something = True
                count += 1
                print("found a thing")
            elif self.read_distance() > trigger_distance and found_something:
                found_something = False
                print("I have a clear view")
        self.stop()
        print("i found this many things: %d" % count)
        return count

    def quick_check(self):
        #Three quick checks
        for ang in range(self.MIDPOINT-250, self.MIDPOINT+251, 250):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False
        
        
        return True

    def nav(self):

        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        
        corner_count = 0
        self.EXIT_HEADING = self.get_heading()
        
        while True:    
            self.servo(self.MIDPOINT)
            while self.quick_check():
                corner_count = 0
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.scan()
            # turns out of cornoer if stuck
            corner_count += 1
            if corner_count == 3:
                self.turntoexit()
            #traversal
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0
            for ang, dist in self.scan_data.items():
                if ang < self.MIDPOINT: 
                    right_total += dist
                    right_count += 1
                else:
                    left_total += dist
                    left_count += 1
            left_avg = left_total / left_count
            right_avg = right_total / right_count
            if left_avg > right_avg:
                self.turn_by_deg(-45)
            else:
                self.turn_by_deg(45)


            # self.turn_by_deg(46)

    def turntoexit(self):
        #turns to favor the exit side
        self.turn_by_deg(180)
        self.deg_fwd(720)
        self.turn_by_deg(self.EXIT_HEADING)
    
    def checkways():
        #smart attempt
        self.servo(1000)
        time.sleep(.3)
        r = self.read_distance()
        self.servo(2000)
        time.sleep(.3)
        l = self.read_distance()
        if l > r:
            self.turn_by_deg(-90)
        if l < r:
            self.turn_by_deg(90)


    def shuffle(self):
        """does the shuffle by wiggles than goes back"""
        # check to see it i safe
        if not self.safe_to_dance():
            print("Nope not doin it")
            return
        else:
            print("fine i'll do it")
        for x in range(5):
            self.right()
            time.sleep(.5)
            self.left()
            time.sleep(.5)
            self.back()
            time.sleep(.5)
            self.right()
            time.sleep(.5)
            self.left()
            time.sleep(.5)
            self.back()
            self.stop()
            

    def safe_to_dance(self):
        for x in range(4):
            for ang in range(1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True
        
    
    def wiggle(self):
        """move left to right really fast"""
        # move left wheel
        for x in range(10):
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.turn_by_deg(180)
            self.stop()

    
    def crazy(self):
        """moves in a box but wiggles"""
        for x in range(20):
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.fwd()
            time.sleep(.1)
            self.turn_by_deg(45)
            self.stop()

           
    
    def itdances(self):
        """does a 180 than snakes and goes back"""
        for x in range(3):
            self.turn_by_deg(180)
            time.sleep(.1)
            self.fwd()
            time.sleep(1)
            self.right()
            time.sleep(1)
            self.left()
            time.sleep(1)
            self.back()
            time.sleep(1)
            self.stop()


            
        
    ###########
    ## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
