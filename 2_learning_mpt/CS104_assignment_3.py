import numpy as np 
import matplotlib.pyplot as plt

rs = np.random.RandomState(seed=42) # instantiate the random state object
betaPlt = rs.beta(a=4, b=20, size=10_000) * 100

expPlt = rs.exponential(scale=0.1, size=(10_000)) * 100

gammaPlt = rs.gamma(scale=0.1, shape=2, size=(10_000)) * 100

lapPlt = rs.laplace(scale=0.5, loc=0, size=(10_000)) * 100

normalPlt = rs.normal(scale=3, loc=0, size=(10_000))

poissonPlt = rs.poisson(lam=3, size=(10_000))

# plot
fig, axs = plt.subplots(nrows=3, ncols=2)

axs[0,0].hist(betaPlt, range=(-5,50), bins=25)

axs[0,1].hist(expPlt, range=(-1,50), bins=25)

axs[1,0].hist(gammaPlt, range=(-1,50), bins=25)

axs[1,1].hist(lapPlt, range=(-1,50), bins=25)

axs[2,0].hist(normalPlt, range=(-10,11), bins=25)

axs[2,1].hist(poissonPlt, range=(-1,11), bins=25)
plt.show()


