# pidcontrol for EvapoRate  version 0.3 written by HR@KIT 2011/2012
#
# version 0.3 tries to make everything more consistent and transparent.
# TODO:  make everything thread safe.

class pidcontrol(object):
    def __init__(self):
        self.Debug = True
        #self.data = data
        #self.hold = False
        
        # target value
        self.ctrl_value = 0
        # initial correction value
        self.correcting_value = 0
        
        # PID parameters
        self.P = 0.00004  # proportional gain
        self.I = 0.00004  # integral gain
        self.D = 0.00001  # derivative gain

        
        self.dState = 0 # Last position input
        self.iState = 0 # Integrator state
        
        self.iMax  = 0.1  # Maximum allowable integrator state
        self.iMin  = -0.001  # Minimum allowable integrator state

    def set_P(self, P):
        self.P = P
    def set_I(self,I):
        self.I = I
    def set_D(self,D):
        self.D = D
    def set_hold(self,state=False):
        self.hold = state
    def set_ctrl_value(self,ctrl_value):
        self.ctrl_value = ctrl_value
        
    def get_error(self,measured_value):
        return self.ctrl_value-measured_value # error value
    
    # this is the main function to be called periodically
    def get_correcting_value(self,measured_value):
        error = self.get_error(measured_value)
        return self.updatePID(error,measured_value),error

    # PID function
    def updatePID(self,error,reading):
        "PID algorithm, returns the correcting value "
        pTerm = 0
        dTerm = 0
        iTerm = 0
        #calculate the proportional term
        pTerm = self.P * error
        
        #calculate the integral state with appropriate limiting
        self.iState += error
        if self.iState > self.iMax:
            self.iState = self.iMax
        if self.iState < self.iMin:
            self.iState = self.iMin
        
        iTerm = self.I * self.iState; # calculate the integral term
        dTerm = self.D * ( reading - self.dState)
        self.dState = reading
        if self.Debug:
            print "P:%.5f I:%.5f D:%.5f terms" %(pTerm,iTerm,dTerm)
            print "I:%.5f D:%.5f states" %(self.iState,self.dState)
        
        self.correcting_value = pTerm + iTerm - dTerm
        return self.correcting_value

    
    #legacy functions
    def update_Heat(self,measured_Temperature):    
        return get_correcting_value(measured_Temperature)
    def update_Rate(self,measured_Rate):
        return get_correcting_value(measured_Rate)
    def set_target_temperature(self,T_set):
        self.target_temperature = T_set    
