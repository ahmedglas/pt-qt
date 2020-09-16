import sys
import os
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath('../simulateur'))
sys.path.insert(0, os.path.abspath('simulateur/'))

from simulateur import (types_recurrents, derouleur, gui, verificateur,
                        gestion_fichiers)
