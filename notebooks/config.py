# Configuracion compartida para notebooks de Fase 2
# CRISP-DM: Comprension de los Datos
# Uso: from config import *

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import json
import warnings
warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

RAW = os.path.join("..", "data", "raw")
FIGS = os.path.join("..", "docs", "figures")
PROC = os.path.join("..", "data", "processed")
os.makedirs(FIGS, exist_ok=True)
os.makedirs(PROC, exist_ok=True)
