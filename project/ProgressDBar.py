class color:
   PURPLE = '\033[1;35;48m'
   CYAN = '\033[1;36;48m'
   BOLD = '\033[1;37;48m'
   BLUE = '\033[1;34;48m'
   GREEN = '\033[1;32;48m'
   YELLOW = '\033[1;33;48m'
   RED = '\033[1;31;48m'
   BLACK = '\033[1;30;48m'
   UNDERLINE = '\033[4;37;48m'
   END = '\033[1;37;0m'

import IPython
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class ProgressTrain():
    def __init__(self,imax,Size=50, num_update=100,names = [],epoch_names = ["Train","Test"]):
        self.imax=imax
        self.i=0
        self.Scale=Size/imax
        self.Size=Size
        self.value_hist = []
        self.names = names
        self.update_rate = int(imax//num_update+1)
        self.epoch = 1

        self.out = display(IPython.display.Pretty('Starting'), display_id=True) #
        time.sleep(0.5)

        self.colorList=[color.RED,color.YELLOW,color.PURPLE,color.BLUE,color.CYAN,color.GREEN]
        self.colorList=[x.replace('8m','8m') for x in self.colorList]

        string = ""
        for name in ["Remaining Time"]+names:
            string += self.show(name,n = max(9,len(name))) + ' || '

        epoch_string = ""
        for name in epoch_names:
            epoch_string += self.show(name) + ' || '
        self.epoch_names = ["Train Loss","Test Loss"] + epoch_names

        print("-"*(Size+10)+"|| "+string)
        if epoch_string == "":
            print("||----||   Epoch   ||          Loss          || ")
            print("||----||   Time    ||   Train   ||   Test    || ")
        else:
            print("||----||   Epoch   ||          Loss          || "+"Others".center(len(epoch_string)-4)+" ||")
            print("||----||   Time    ||   Train   ||   Test    || "+epoch_string)
        time.sleep(0.5)

        self.start_time = time.time()

        self.update()
        
    def update(self,x=[]):
        if self.i%self.update_rate == 0:

            Color=self.colorList[min(len(self.colorList)-1,round(self.i/self.imax*(len(self.colorList)-1)))]

            def format_number(x, n=5):
                return "{:>{width}.2f}".format(x, width=n)
            
            def format_delta_time(delta):
                hours = int(delta // 3600)
                minutes = int((delta % 3600) // 60)
                seconds = int(delta % 60)
                return "{:02}h{:02}m{:02}s".format(hours, minutes, seconds)
            
            if self.i == 0:
                remaining_time = 0
            else:
                remaining_time = (time.time()-self.start_time)*(self.imax/(self.i+0.0001)-1)

            x = [format_delta_time(remaining_time)] + x

            string = Color+'['+'%'*round(self.i*self.Scale)+'-'*round((self.imax-self.i)*self.Scale)+'] '+format_number(100*self.i/(self.imax))+'%'+color.END
            string += color.BOLD
            for value,name in zip(x,["Remaining Time"]+self.names):
                string += ' || '+self.show(value,n = max(9,len(name)))

            string += color.END+' ||   '

            self.out.update(IPython.display.Pretty(string))
            time.sleep(0.01)
        
        self.i+=1

    def show(self,x,n=9,c=None):
        if n<5:
            assert "To short to show"
        if type(x)==int or type(x)==float:
            if (x>=(10**4) or x<=(10**(-4))) and x >0:
                out = ("{:."+str(n-6)+"e}").format(x)
            elif (x<=-(10**4) or x>=-(10**(-4))) and x < 0:
                out = ("{:."+str(n-7)+"e}").format(x)
            else:
                out = str(x)[:n]
        elif type(x)==str:
            
            if len(x)>n:
                out = x[:n]
            else:
                out = x.center(n)
        else:
            out = str(x)[:n]
        
        if c is None:
            return out + " "*max((n-len(out)),0)
        else:
            return c + out + " "*max((n-len(out)),0) + color.END
        

    def end(self,x=[],kaggle = False):
        self.i-=1

        def format_integer(x, n=3):
            return "{:>{width}}".format(x, width=n)
        
        def format_delta_time(delta):
                hours = int(delta // 3600)
                minutes = int((delta % 3600) // 60)
                seconds = int(delta % 60)
                return "{:02}h{:02}m{:02}s".format(hours, minutes, seconds)
            
        total_time = time.time()-self.start_time

        x = [format_delta_time(total_time)] + x
        
        if self.i==self.imax:
            string = '||'+color.GREEN+format_integer(self.epoch)+color.END #+'' + color.BOLD
            
        else:
            string = color.YELLOW+'||'+format_integer(self.epoch)+color.END+'' + color.BOLD
        for k, value in enumerate(x):
            if self.epoch == 1 or k==0:
                string += ' || '+self.show(value)
            else:
                if value < self.value_hist[-1][k-1]:
                    if k>2:
                        string += ' || '+self.show(value,c = color.RED)
                    else:
                        string += ' || '+self.show(value,c = color.GREEN)
                elif value > self.value_hist[-1][k-1]:
                    if k>2:
                        string += ' || '+self.show(value,c = color.GREEN)
                    else:
                        string += ' || '+self.show(value,c = color.RED)
                else:
                    string += ' || '+self.show(value)
        
        string += ' || '
        self.i=0
        self.update()
        self.value_hist.append(x[1:])
        self.epoch += 1
        self.start_time = time.time()

        if kaggle:
            return string
        else:
            print(string)
        

        
    def get(self,input_names):

        data = np.transpose(np.array(self.value_hist))
        if not isinstance(input_names, list):
            input_names = [input_names]
        # Find indices of the input names
        indices = [self.epoch_names.index(name) for name in input_names if name in self.epoch_names]
        # Extract and return the data for these indices
        return [data[index] for index in indices]

    def plot(self, input_names = ["Train Loss","Test Loss"]):

        data = np.transpose(np.array(self.value_hist))
        # Ensure input_names is a list
        if isinstance(input_names, str):
            input_names = [input_names]
        
        plt.figure(figsize=(10, 4)) 
        # Plot data for each name in input_names
        for name in input_names:
            if name in self.epoch_names:
                index = self.epoch_names.index(name)
                plt.plot(range(1,len(data[index])+1),data[index], label=name)

        # Set plot features
        plt.xlabel('Epoch')
        plt.ylabel('Value')
        plt.title(', '.join(input_names)+ " Evolution.")
        plt.legend()
        #plt.grid()
        
        ax = plt.gca()
        ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        
        plt.show()