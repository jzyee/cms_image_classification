# Scientific-Poster Content
## Poster Skeleton
- Abstract
- Introduction
  - Collision Model
  - CNN Model
- Background
  - Convolutional Neural Networks (CNN)
  - The Large Hadron Collider (LHC)
  - Compact Muon Solenoid (CMS) 
- Methodology
- Result
- Reference

## Abstract
The program of LHC and CMS records the collision of high energy physics and shares the data in the worldwide LHC Computing Grid, which gives a platform for physicists in 42 countries. This research applied convolutional neural network to particle collisions classification. We compare the performance of four well-known convolutional neural network and test transfer learning in particle classification.

## Introduction
### Collision Model (Top quark pair events:)
We focus on the production of a pair of quarks top anti-top (ttbar) and discriminate them from other processes (background). 
- Each top quark decays into a W boson and a bottom quark.
- One of W bosons decays leptonically into a charged lepton, electron or muon, with an associated neutrino.
- Background:
       - W + jets events
       - Drell-Yan processes

### CNN models:
- InceptionV3: achieves state-of-the-art accuracy for recognizing general objects with 1000 classes.
- VGG16,VGG19: Same architecture with different depth.
- oResNet50: Trained from a million images from the ImageNet database.

##Background
###Convolutional Neural Networks (CNN)
CNN is widely used in the computer vision community to fix complex issues, it consists of convolutional layers and forward-passing fully connected layers.
###The Large Hadron Collider (LHC)
Large Hadron Collider (LHC) is the world’s largest particle collider and is used to accelerate particles beams and guide particle’s collision. These particles can be detected by the detector - CMS.
###Compact Muon Solenoid (CMS) 
Compact Muon Solenoid (CMS) is a particle detector, like a cylindrical onion, has different layers to measure different properties of particles.

## Methodology
### Process
- Overview
 
Figure 1 Flow Chart

We use Open Data Monte Carlo samples of collisions at LHC from CMS Open Data portal to create images containing information of different physics observables. Then we train the convolutional neural network on these images to distinguish the different physics process.

- Getting data & Creating JSON
- Data Type: AODSIM root files
Collisions, also known as events, recorded in a HEP experiment by a detector like CMS. Ana these events are described by a set of variables: the momentum of muons, electrons, photons and hadrons produced in the collision of the two accelerated protons, which have been released as Open Data by the CMS collaboration

- JSON file: Containing the main information on the physics observables. 

- Flow: Create a link to condition database and download the target index respectively. Generate JSON using a C++ framework based on a template provided by the Open Data group.

### Images Creation
- All the observables are to be represented using a canvas of dimension 224×224 pixels. Each particle or physics object is represented as a circumference with a radius proportional to its energy.
- The momentum direction coordinates the pseudorapidity η and the azimuthal angle φ
- Color: different type of particles and physics objects

 
Figure 2 Image Representaion

In our experiment:
 
Figure 3 Image in our experiment

- **Circumferences**: Leptons and Jets
- **Radius**: proportional to transverse momentum

             Scale: Pt’ = C * ln (pt)   (C ~ 10.5)

- **Color**:
- **blue** for the **electrons**
- **green** for the **muons**
- **light red** for **non-B-tagged jets**
- **dark red** for **B-tagged jets**
- **Black** for **missing transverse energy**

### Classifying images by Transfer Learning technique


## Result
## Reference





