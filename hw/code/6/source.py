from models import Schaffer, Osyczka2, Kursawe
from optimizers import sa, mws

for model in [Schaffer, Osyczka2, Kursawe]:
  for optimizer in [sa, mws]:
     optimizer(model())