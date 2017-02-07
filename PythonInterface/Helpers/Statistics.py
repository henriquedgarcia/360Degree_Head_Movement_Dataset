"""Functions/Classes to compute statistics on test logs.

Author: Xavier Corbillon
IMT Atlantique
"""

import Helpers.Quaternion as Q
import math
import numpy as np
import matplotlib.pyplot as plt


def GetAngularVelocityList(pathToFile):
    """Get the angular velocity vector based on a log file."""
    qList = list()
    tList = list()
    angVelDict = dict()
    with open(pathToFile, 'r') as i:
        for line in i:
            values = line.split(' ')
            qList.append(Q.Quaternion(w=float(values[2]),
                                      v=Q.Vector(x=float(values[3]),
                                                 y=float(values[4]),
                                                 z=float(values[5])
                                                 )
                                      )
                         )
            tList.append(float(values[0]))
            if len(qList) == 3:
                q1 = qList[0]
                q2 = qList[1]
                q3 = qList[2]

                velocity = (Q.Quaternion.Distance(q1, q2) +
                            Q.Quaternion.Distance(q2, q3))/2
                velocity /= (tList[2]-tList[0])
                angVelDict[tList[1]] = velocity

                qList = qList[1:]
                tList = tList[1:]
        return angVelDict


def PrintAngularVelocityDictStats(angVelDict):
        """Print some statistics on the angular velocity."""
        angVelList = angVelDict.values()
        print('Mean angular velocity: ', sum(angVelList)/len(angVelList),
              ' -> in deg: ', (180/math.pi)*sum(angVelList)/len(angVelList))
        print('Min angular velocity: ', min(angVelList), ' -> in deg: ',
              (180/math.pi)*min(angVelList))
        print('Max angular velocity: ', max(angVelList), ' -> in deg: ',
              (180/math.pi)*max(angVelList))


def GetPositionMatrix(pathToFile, W=50, H=50):
    """Generate a position matrix based on a list file."""
    pos = np.zeros((W, H))
    with open(pathToFile, 'r') as i:
        for line in i:
            values = line.split(' ')
            q = Q.Quaternion(w=float(values[2]),
                             v=Q.Vector(x=float(values[3]),
                                        y=float(values[4]),
                                        z=float(values[5])
                                        )
                             )
            v = q.Rotation(Q.Vector(1, 0, 0)).v
            theta, phi = v.ToPolar()
            i = int(W*(theta + math.pi)/(2*math.pi))
            j = int(H*phi/math.pi)
            pos[j, i] += 1

    return pos


def PlotPositions(posMat):
    """Plot a position matrix."""
    plt.matshow(posMat)
    plt.show()
