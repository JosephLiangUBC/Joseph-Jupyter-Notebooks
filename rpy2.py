packnames = ('lme4', 'lmerTest', 'emmeans', "geepack", "afex", "dplyr")
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector
utils = importr("utils")
utils.chooseCRANmirror(ind=1)
utils.install_packages(StrVector(packnames))