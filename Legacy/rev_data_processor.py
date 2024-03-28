#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:22:43 2019

@author: alex

This script is to replace Matlab IPA script
"""
#import libraries
import os
import numpy as np
import pandas as pd

#user input
preplate=300 #acclimatization period
isi=10 #inter-stimulus interval
nstim=30 #number of stimuli
dt=1 #criterion for response
suffix='.trv' #tap or light pulse

#initialize stim onset array
onset=np.linspace(preplate,preplate+isi*(nstim-1),nstim)
offset=onset+dt

#loop through folders
root_path=os.getcwd()
strain_list=[strain for strain in os.listdir() if os.path.isdir(strain)] #list all strain folders
for strainID in strain_list: #loop through each strain folder
    os.chdir(os.path.join(root_path,strainID))
    strain_path=os.getcwd()
    prob_strain = np.array([]).reshape(0,2)
    dist_strain = np.array([]).reshape(0,2)
    dura_strain = np.array([]).reshape(0,2)
    spd_strain = np.array([]).reshape(0,2)
    lat_strain = np.array([]).reshape(0,2)
    plate_list=[plate for plate in os.listdir() if os.path.isdir(plate)] #list all plate folders
    for plateID in plate_list: #loop through each plate folder
        os.chdir(os.path.join(strain_path,plateID))
        worm_data=np.array([]).reshape(0,4)
        for rev in os.listdir(): #load trv/prv and txt files in each folder
            if rev.endswith(suffix):
                plate_data=np.loadtxt(rev)
            if rev.endswith('.txt'):
                worm_data=np.vstack((worm_data,np.loadtxt(rev)))
        stim_onset=plate_data[:,0] #check for correct number of stims
        if stim_onset.size!=nstim:
            print("fix stim number in " + plateID + "!!!")
            break
        else:
            stimID=np.arange(nstim)+1
            prob_plate=plate_data[:,3]/(plate_data[:,2]+plate_data[:,3]) #sort prob data from trv/prv
            prob_plate=np.vstack([stimID,prob_plate]).T
            prob_strain=np.vstack([prob_strain,prob_plate]) 
            dist_plate=np.array([])
            dura_plate=np.array([])
            spd_plate=np.array([])
            lat_plate=np.array([])
            for i in range(nstim): # sort dist, dura, spd, lat, from txt
                response_bool=(worm_data[:,1]>=stim_onset[i]) & (worm_data[:,1]<=stim_onset[i]+dt) #flag response
                stim_data=worm_data[response_bool]
                dist_stim=stim_data[:,2]
                dura_stim=stim_data[:,3]
                spd_stim=stim_data[:,2]/stim_data[:,3]
                lat_stim=stim_data[:,1]-stim_onset[i]
                dist_plate=np.append(dist_plate,np.nanmean(dist_stim))
                dura_plate=np.append(dura_plate,np.nanmean(dura_stim))
                spd_plate=np.append(spd_plate,np.nanmean(spd_stim))
                lat_plate=np.append(lat_plate,np.nanmean(lat_stim))
            dist_plate=np.vstack([stimID,dist_plate]).T
            dist_strain=np.vstack([dist_strain,dist_plate]) 
            dura_plate=np.vstack([stimID,dura_plate]).T
            dura_strain=np.vstack([dura_strain,dura_plate]) 
            spd_plate=np.vstack([stimID,spd_plate]).T
            spd_strain=np.vstack([spd_strain,spd_plate]) 
            lat_plate=np.vstack([stimID,lat_plate]).T
            lat_strain=np.vstack([lat_strain,lat_plate]) 
            os.chdir(strain_path)
    revProf={'Stim':prob_strain[:,0],
             'Prob':prob_strain[:,1],
             'Dist':dist_strain[:,1],
             'Dura':dura_strain[:,1],
             'Spd':spd_strain[:,1],
             'Lat':lat_strain[:,1],
             'Plate':pd.Series([plate_list[j] for j in range(len(plate_list)) for k in range(nstim)]),
             'Strain':pd.Series([strainID for l in range(nstim*len(plate_list))])}
    df=pd.DataFrame(revProf)
    np.savetxt(strainID+'.pyprob',prob_strain,delimiter=' ') #save prob file
    np.savetxt(strainID+'.pydist',dist_strain,delimiter=' ') #save dist file
    np.savetxt(strainID+'.pydura',dura_strain,delimiter=' ') #save dura file
    np.savetxt(strainID+'.pyspd',spd_strain,delimiter=' ') #save spd file
    np.savetxt(strainID+'.pylat',lat_strain,delimiter=' ') #save lat file
    df.to_csv(strainID+'.pyrev',sep=' ',index=0) #save revProf file
    os.chdir(root_path)
    
    
