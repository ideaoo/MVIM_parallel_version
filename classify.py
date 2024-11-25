import numpy as np
import datetime
import pandas as pd



starttime = datetime.datetime.now()



# the path of the input file

for x in range(0,2):
    globals()['path_'+str(x)] = "D:/parallel_mvim/new_2/decimal_arranged/average_arrange_%s.dump"%(x)
    
    # the folder of the final files
    globals()['path'+str(x)] = "D:/parallel_mvim/new_2/decimal_arranged/part%s"%(x)
    



# the pieces to be divided 
pieces = 8

# the pieces to be divided into in each dimension
part = float(np.cbrt(pieces))

tol = 35.0

for x in range(0,2):
# open the files of the references and the targets 
    for i in range(pieces):

        globals()['fdata'+str(i)] = open(globals()['path'+str(x)]+'/file_%s.dump'%(i), 'w')
        globals()['ref'+str(i)] = open(globals()['path'+str(x)]+'/ref_%s.dump'%(i), 'w')


    # Read the information of the header
    Bars = []
    data = open(globals()['path_'+str(x)],'r')

    for i in range (9):
        line = data.readline()
        Bars.append(line)

    data.close()
    natom = Bars[3]
    natoms = int(natom)

    X = Bars[5]
    Y = Bars[6]
    Z = Bars[7]
        
    BoundaryX = X.split()
    BoundaryXMIN = float(BoundaryX[0])
    BoundaryXMAX = float(BoundaryX[1])
    value_X = BoundaryXMAX/part


    BoundaryY = Y.split()
    BoundaryYMIN = float(BoundaryY[0])
    BoundaryYMAX = float(BoundaryY[1])
    value_Y = BoundaryYMAX/part


    BoundaryZ = Z.split()
    BoundaryZMIN = float(BoundaryZ[0])
    BoundaryZMAX = float(BoundaryZ[1])
    value_Z = BoundaryZMAX/part


    # Separate the file into different files with several conditions
    with open(globals()['path_'+str(x)],'r') as f:

        for i in range(pieces):

            locals()['Counter'+str(i)] = 0

        for i in range(pieces):

            locals()['counter'+str(i)] = 0

        for n_of_lines in range (1,natoms+10):
            lines_after_10 = f.readline()

            if n_of_lines > 9:
                  
                a = lines_after_10.split()

                TYPE = int(a[1])
                Aposition = a[2:5]
                position = [float(i) for i in Aposition]
                
                if TYPE != 3 :

                    Coordinate_value = abs(position[0])//value_X + abs(position[1])//value_Y*part + abs(position[2])//value_Z*np.square(part)

                    Flag_X = 0
                    Flag_Y = 0
                    Flag_Z = 0

                    if -1.0*tol <= position[0] - value_X <= 0.0 or -1*tol <= position[0] - BoundaryXMIN <= tol :
                        Flag_X = 1

                    if  0.0 <= position[0] - value_X <= tol or -1*tol <= position[0] - BoundaryXMAX <= tol : 
                        Flag_X = -1

                    if -1.0*tol <= position[1] - value_Y <= 0.0 or -1*tol <= position[1] - BoundaryYMIN <= tol :
                        Flag_Y = part

                    if  0.0 <= position[1] - value_Y <= tol or -1*tol <= position[1] - BoundaryYMAX <= tol :
                        Flag_Y = -1*part

                    if -1.0*tol <= position[2] - value_Z <= 0.0 or -1*tol <= position[2] - BoundaryZMIN <= tol :
                        Flag_Z = np.square(part)

                    if  0.0 <= position[2] - value_Z <= tol or -1*tol <= position[2] - BoundaryZMAX <= tol :
                        Flag_Z = -1*np.square(part)

                    
                    if  Flag_X != 0 :
                        Overlap_value_X = Coordinate_value + Flag_X 

                    else :
                        Overlap_value_X = -100


                    if  Flag_Y != 0 :
                        Overlap_value_Y = Coordinate_value + Flag_Y
                    
                    else:
                        Overlap_value_Y = -100
                        

                    if  Flag_Z != 0 :
                        Overlap_value_Z = Coordinate_value + Flag_Z 

                    else:
                        Overlap_value_Z = -100


                    if Flag_X and Flag_Y != 0 :
                        Overlap_value_diag0 = Coordinate_value + Flag_X + Flag_Y

                    else :
                        Overlap_value_diag0 = -100
                    

                    if Flag_X and Flag_Z != 0 :
                        Overlap_value_diag1 = Coordinate_value + Flag_X + Flag_Z

                    else :
                        Overlap_value_diag1 = -100
                        

                    if Flag_Y and Flag_Z != 0 :
                        Overlap_value_diag2 = Coordinate_value + Flag_Y + Flag_Z
                    
                    else :
                        Overlap_value_diag2 = -100


                    if Flag_X and Flag_Y and Flag_Z != 0 :
                        Overlap_value_diag3 = Coordinate_value + Flag_X + Flag_Y + Flag_Z

                    else :
                        Overlap_value_diag3 = -100


                    if Coordinate_value == 0 :

                        fdata0.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                            

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                    

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                            

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                            

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            

                    elif Coordinate_value == 1 :

                        fdata1.write(lines_after_10)
                       

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                           

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                            

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                           

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                           

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                           

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                           

                    elif Coordinate_value == 2 :

                        fdata2.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                            

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                        

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                           

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                            

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                            

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            

                    elif Coordinate_value == 3 :

                        fdata3.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                            

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                           

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                            

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                           

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            

                    elif Coordinate_value == 4 :

                        fdata4.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                           

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                            

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                             

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                            

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            

                    elif Coordinate_value == 5 :

                        fdata5.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                          

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                           

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                            

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                            

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            

                    elif Coordinate_value == 6 :

                        fdata6.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                          

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                            

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                            

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                            

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                            

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            
                    
                    elif Coordinate_value == 7 :

                        fdata7.write(lines_after_10)
                        

                        if Overlap_value_X == 0 or Overlap_value_Y == 0 or Overlap_value_Z == 0 or Overlap_value_diag0 == 0 or Overlap_value_diag1 == 0 or Overlap_value_diag2 == 0 or Overlap_value_diag3 == 0 :
                            ref0.write(lines_after_10)
                            fdata0.write(lines_after_10)
                           

                        if Overlap_value_X == 1 or Overlap_value_Y == 1 or Overlap_value_Z == 1 or Overlap_value_diag0 == 1 or Overlap_value_diag1 == 1 or Overlap_value_diag2 == 1 or Overlap_value_diag3 == 1 :
                            ref1.write(lines_after_10)
                            fdata1.write(lines_after_10)
                            

                        if Overlap_value_X == 2 or Overlap_value_Y == 2 or Overlap_value_Z == 2  or Overlap_value_diag0 == 2 or Overlap_value_diag1 == 2 or Overlap_value_diag2 == 2 or Overlap_value_diag3 == 2 :
                            ref2.write(lines_after_10)
                            fdata2.write(lines_after_10)
                            

                        if Overlap_value_X == 3 or Overlap_value_Y == 3 or Overlap_value_Z == 3 or Overlap_value_diag0 == 3 or Overlap_value_diag1 == 3 or Overlap_value_diag2 == 3 or Overlap_value_diag3 == 3 :
                            ref3.write(lines_after_10)
                            fdata3.write(lines_after_10)
                            

                        if Overlap_value_X == 4 or Overlap_value_Y == 4 or Overlap_value_Z == 4 or Overlap_value_diag0 == 4 or Overlap_value_diag1 == 4 or Overlap_value_diag2 == 4 or Overlap_value_diag3 == 4 :
                            ref4.write(lines_after_10)
                            fdata4.write(lines_after_10)
                            

                        if Overlap_value_X == 5 or Overlap_value_Y == 5 or Overlap_value_Z == 5 or Overlap_value_diag0 == 5 or Overlap_value_diag1 == 5 or Overlap_value_diag2 == 5 or Overlap_value_diag3 == 5 :
                            ref5.write(lines_after_10)
                            fdata5.write(lines_after_10)
                         

                        if Overlap_value_X == 6 or Overlap_value_Y == 6 or Overlap_value_Z == 6 or Overlap_value_diag0 == 6 or Overlap_value_diag1 == 6 or Overlap_value_diag2 == 6 or Overlap_value_diag3 == 6 :
                            ref6.write(lines_after_10)
                            fdata6.write(lines_after_10)
                            

                        if Overlap_value_X == 7 or Overlap_value_Y == 7 or Overlap_value_Z == 7 or Overlap_value_diag0 == 7 or Overlap_value_diag1 == 7 or Overlap_value_diag2 == 7 or Overlap_value_diag3 == 7 :
                            ref7.write(lines_after_10)
                            fdata7.write(lines_after_10)
                            

                else :
                    continue


endtime = datetime.datetime.now()
print(endtime - starttime)
print("done")

