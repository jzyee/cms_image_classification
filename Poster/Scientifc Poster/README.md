# Scientific-Poster Content
## Poster Skeleton
- Abstract
- Introduction
  - LHC & CMS
  - Deep learning CNNs
  - Top quark pair events
- Methodology
- Result
- Reference

## Abstract
Use deep learning model to analyze the data from the CMS Open Data portal. Specifically, we use the image classification which is an application of CNNs in the context of analysis in experimental High Energy Physics (HEP).

## Introduction
### LHC & CMS
LHC (The Large Hadron Collider) the world’s largest particle collider, is used to accelerate particles beams and guide the particle’s collision. CMS (Compact Muon Solenoid) is a particle detector, like a cylindrical onion, has different layers to measure different properties of particles.

### Deep Learning (CNN)
Deep learning with convolutional neural networks (CNNs) is one of the most widely effective methods in computer vision and speech recognition for past few years, which gives us the probabilities to apply it in particle physics analysis.

### Top quark pair events
We focus on the production of a pair of quarks top anti-top (ttbar) and discriminate them from other processes (background).
- Top quark pair events: 
    - Each top quark decays into a W boson and a bottom quark.
    - One of W bosons decays leptonically into a charged lepton, electron or muon, with an associated neutrino.
    - Background:
- W + jets events
- Drell-Yan processes
 
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





