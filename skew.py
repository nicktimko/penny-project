from scipy import linspace
from scipy import pi,sqrt,exp
from scipy.special import erf
from scipy.optimize import leastsq
from scipy.stats import norm

from pylab import plot,show

#def pdf(x):
#    return 1/sqrt(2*pi) * exp(-x**2/2)

#def cdf(x):
#    return (1 + erf(x/sqrt(2))) / 2

def skew(x,e=0,w=1,a=0):
    t = (x-e) / w
    #return 2 / w * pdf(t) * cdf(a*t)
    # You can of course use the scipy.stats.norm versions
    return 2 * norm.pdf(t) * norm.cdf(a*t)

if __name__ == '__main__':
    n = 2**10

    e = 1.0 # location
    w = 2.0 # scale

    x = linspace(-10,10,n) 

    for a in range(-3,4):
        p = skew(x,e,w,a)
        plot(x,p)

    fzz = skew(x,e,w,a) + norm.rvs(0,0.04,size=n) # fuzzy data

    def optm(l,x):
        return skew(x,l[0],l[1],l[2]) - fzz

    print leastsq(optm,[0.5,0.5,0.5],(x,))

    show()