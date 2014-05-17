import random

import provider
import tripler
import researcher

behaviors = [provider.Provider(), tripler.Tripler(), researcher.Researcher()]
#behaviors = [researcher.Researcher()]

for _ in xrange(20):
    chosen_behavior = random.choice(behaviors)
    chosen_behavior.run()
