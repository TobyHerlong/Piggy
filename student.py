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
        self.LEFT_DEFAULT = 80
        self.RIGHT_DEFAULT = 80
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?
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
            #self.shuffle()
            #self.wiggle()
            self.crazy()
            #self.itdances()
            
    
    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-350, self.MIDPOINT+350, 3):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        print("I can't count how many obstacles are around me. Please give my programmer a zero.")

    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")

    def shuffle(self):
        """spin around"""
        # check to see it i safe
        if not self.safe_to_dance():
            print("Nope not doin it")
            return
        else:
            print("fine i'll do it")
        self.fwd()
        for x in range(1):
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
        """move left to right"""
        # move left wheel
        if not self.safe_to_dance():
            print("Nope not doin it")
            return
        else:
            print("fine i'll do it")
        for x in range(20):
            self.right()
            time.sleep(.1)
            self.left()
            time.sleep(.1)
            self.stop()

    
    def itdances(self):
        """moves the robot left and right forward then backwards"""
        # move left wheel forward
        pass      
    
    def crazy(self):
        """spins and moves servo"""
        if not self.safe_to_dance():
            print("Nope not doin it")
            return
        else:
            print("fine i'll do it")
        for x in range(1):
            self.servo(1000)
            time.sleep(.1)        
            self.left()
            time.sleep(.5)      
            self.servo(1500)
            time.sleep(.1)
            self.right()
            time.sleep(.5)
            self.turn_by_deg(180)
            time.sleep(.1)
            self.fwd(2)
            time.sleep(.3)
            self.right()
            time.sleep(.3)
            self.left()
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
