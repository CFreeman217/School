# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2018 replay file
# Internal Version: 2017_11_07-11.21.41 127140
# Run by ctf365 on Thu Dec  6 16:06:18 2018
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=282.359375, 
    height=141.108322143555)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('finalProject.cae')
#: The model database "D:\School\Finite_Elements_ME486\finalProject.cae" has been opened.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.845, 
    farPlane=32.1449, width=16.003, height=6.84219, viewOffsetX=1.27203, 
    viewOffsetY=-0.0788239)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.0582, 
    farPlane=32.9316, width=23.2744, height=9.95115, viewOffsetX=1.21595, 
    viewOffsetY=-0.0753487)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.1318, 
    farPlane=32.8581, width=23.3748, height=9.99407, cameraPosition=(16.5457, 
    12.5987, 17.0025), cameraUpVector=(-0.873336, -0.163039, 0.459024), 
    cameraTarget=(2.11482, -1.83215, 2.57166), viewOffsetX=1.22119, 
    viewOffsetY=-0.0756737)
session.viewports['Viewport: 1'].view.setValues(nearPlane=19.2614, 
    farPlane=33.1049, width=26.2805, height=11.2364, cameraPosition=(25.4934, 
    2.53659, 8.39093), cameraUpVector=(-0.544494, 0.736369, 0.401606), 
    cameraTarget=(1.3196, -1.23434, 3.2765), viewOffsetX=1.373, 
    viewOffsetY=-0.0850807)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
mdb.models['Model-1'].Material(name='SS316')
mdb.models['Model-1'].materials['SS316'].Elastic(table=((190000000.0, 0.265), 
    ))
mdb.models['Model-1'].materials['SS316'].Density(table=((7870.0, ), ))
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', 
    material='SS316', thickness=None)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
region = p.Set(cells=cells, name='Set-1')
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, 
    offsetType=MIDDLE_SURFACE, offsetField='', 
    thicknessAssignment=FROM_SECTION)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON, optimizationTasks=OFF, 
    geometricRestrictions=OFF, stopConditions=OFF)
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial', 
    description='TorqueFaceLoading')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=OFF)
a = mdb.models['Model-1'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
a.Instance(name='polemount_2Jeremiah-1-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=OFF, 
    engineeringFeatures=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
p1 = mdb.models['Model-1'].parts['polemount_2Jeremiah-2']
session.viewports['Viewport: 1'].setValues(displayedObject=p1)
del mdb.models['Model-1'].parts['polemount_2Jeremiah-2']
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    adaptiveMeshConstraints=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    adaptiveMeshConstraints=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, interactions=OFF, constraints=OFF, 
    engineeringFeatures=OFF)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['polemount_2Jeremiah-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#2000 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='Surf-1')
mdb.models['Model-1'].Pressure(name='FaceLoad', createStepName='Step-1', 
    region=region, distributionType=UNIFORM, field='', magnitude=5000.0, 
    amplitude=UNSET)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.0471, 
    farPlane=32.9427, width=13.8871, height=6.95347, viewOffsetX=0.56569, 
    viewOffsetY=0.0426721)
mdb.models['Model-1'].loads['FaceLoad'].setValues(distributionType=TOTAL_FORCE)
session.viewports['Viewport: 1'].view.setValues(nearPlane=18.0211, 
    farPlane=31.9688, width=7.4327, height=3.72167, viewOffsetX=1.44813, 
    viewOffsetY=-0.699105)
session.viewports['Viewport: 1'].view.setValues(nearPlane=18.0808, 
    farPlane=31.909, width=7.45735, height=3.73401, viewOffsetX=1.67554, 
    viewOffsetY=-1.25076)
session.viewports['Viewport: 1'].view.setValues(nearPlane=20.3752, 
    farPlane=32.5595, width=8.40365, height=4.20784, cameraPosition=(21.1426, 
    1.03455, 18.7392), cameraUpVector=(-0.327978, 0.925865, -0.187627), 
    cameraTarget=(1.07158, -0.086823, 3.88509), viewOffsetX=1.88816, 
    viewOffsetY=-1.40948)
session.viewports['Viewport: 1'].view.setValues(nearPlane=19.4528, 
    farPlane=33.4819, width=13.1621, height=6.59047, viewOffsetX=1.70558, 
    viewOffsetY=0.539258)
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['polemount_2Jeremiah-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#420 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='Surf-2')
mdb.models['Model-1'].SurfaceTraction(name='Load-2', createStepName='Step-1', 
    region=region, magnitude=6000.0, directionVector=((1.0, 0.0, 0.0), (2.0, 
    0.0, 0.0)), distributionType=UNIFORM, field='', localCsys=None, 
    traction=GENERAL)
session.viewports['Viewport: 1'].view.setValues(nearPlane=20.5078, 
    farPlane=33.6415, width=13.8759, height=6.9479, cameraPosition=(25.4769, 
    0.172461, 11.9988), cameraUpVector=(-0.276352, 0.936808, -0.214523), 
    cameraTarget=(1.83325, 0.23497, 3.89188), viewOffsetX=1.79808, 
    viewOffsetY=0.568504)
session.viewports['Viewport: 1'].view.setValues(nearPlane=21.5605, 
    farPlane=35.92, width=14.5882, height=7.30454, cameraPosition=(22.9301, 
    -3.58887, -14.094), cameraUpVector=(-0.0204934, 0.936234, 0.35078), 
    cameraTarget=(3.45101, -0.897127, 1.33545), viewOffsetX=1.89038, 
    viewOffsetY=0.597686)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Initial')
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['polemount_2Jeremiah-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#141c0 ]', ), )
region = a.Set(faces=faces1, name='Set-1')
mdb.models['Model-1'].DisplacementBC(name='boltHoles', 
    createStepName='Initial', region=region, u1=SET, u2=SET, u3=SET, ur1=SET, 
    ur2=SET, ur3=SET, amplitude=UNSET, distributionType=UNIFORM, fieldName='', 
    localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=22.7439, 
    farPlane=36.8254, width=15.3889, height=7.70547, cameraPosition=(-12.7291, 
    -6.50855, -23.3273), cameraUpVector=(0.549351, 0.82979, -0.0982944), 
    cameraTarget=(-0.861975, -1.77942, -1.84341), viewOffsetX=1.99414, 
    viewOffsetY=0.630492)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.0827, 
    farPlane=36.4868, width=11.4622, height=5.73932, viewOffsetX=1.67015, 
    viewOffsetY=1.51576)
del mdb.models['Model-1'].boundaryConditions['boltHoles']
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.1734, 
    farPlane=36.9552, width=12.0038, height=6.0105, cameraPosition=(18.4258, 
    -1.36266, -21.6402), cameraUpVector=(-0.413148, 0.908706, 0.0596868), 
    cameraTarget=(5.31001, 0.450376, -0.440205), viewOffsetX=1.74906, 
    viewOffsetY=1.58738)
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['polemount_2Jeremiah-1-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1c1c0 ]', ), )
region = a.Set(faces=faces1, name='Set-2')
mdb.models['Model-1'].DisplacementBC(name='BC-1', createStepName='Initial', 
    region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET, 
    amplitude=UNSET, distributionType=UNIFORM, fieldName='', localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.9025, 
    farPlane=37.0805, width=11.8693, height=5.94313, cameraPosition=(28.5928, 
    -2.9612, 13.0449), cameraUpVector=(-0.471912, 0.734771, 0.487248), 
    cameraTarget=(5.03009, -1.33176, 4.86601), viewOffsetX=1.72946, 
    viewOffsetY=1.56959)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
del mdb.models['Model-1'].loads['Load-2']
a = mdb.models['Model-1'].rootAssembly
s1 = a.instances['polemount_2Jeremiah-1-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#420 ]', ), )
region = a.Surface(side1Faces=side1Faces1, name='Surf-3')
mdb.models['Model-1'].SurfaceTraction(name='TorqueLoad', 
    createStepName='Step-1', region=region, magnitude=6000.0, directionVector=(
    (1.0, 0.0, 0.0), (2.0, 0.0, 0.0)), distributionType=UNIFORM, field='', 
    localCsys=None)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.2065, 
    farPlane=35.7765, width=2.66496, height=1.33438, viewOffsetX=1.68071, 
    viewOffsetY=1.21413)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.3649, 
    farPlane=35.4598, width=2.68171, height=1.34277, cameraPosition=(29.6577, 
    -6.41756, 4.93613), cameraUpVector=(-0.262397, 0.687757, 0.676859), 
    cameraTarget=(5.1223, -1.9683, 3.2129), viewOffsetX=1.69127, 
    viewOffsetY=1.22176)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.0429, 
    farPlane=35.7818, width=5.22945, height=2.61847, viewOffsetX=1.8709, 
    viewOffsetY=1.00655)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.2595, 
    farPlane=36.0809, width=5.2747, height=2.64112, cameraPosition=(30.0338, 
    -4.06463, -1.84094), cameraUpVector=(-0.155296, 0.679229, 0.717308), 
    cameraTarget=(5.47678, -1.56345, 2.08926), viewOffsetX=1.88709, 
    viewOffsetY=1.01526)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.7891, 
    farPlane=36.5513, width=9.03408, height=4.52351, viewOffsetX=3.07237, 
    viewOffsetY=0.712501)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.719, 
    farPlane=36.6214, width=9.00853, height=4.51071, cameraPosition=(30.0494, 
    -4.02166, -1.77085), cameraUpVector=(-0.156087, 0.69367, 0.703178), 
    cameraTarget=(5.49237, -1.52048, 2.15935), viewOffsetX=3.06368, 
    viewOffsetY=0.710486)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.7189, 
    farPlane=36.6216, width=9.00848, height=4.51069, cameraPosition=(30.0377, 
    -4.05401, -1.82329), cameraUpVector=(-0.155487, 0.682876, 0.713796), 
    cameraTarget=(5.48068, -1.55283, 2.10691), viewOffsetX=3.06366, 
    viewOffsetY=0.710482)
session.viewports['Viewport: 1'].view.setValues(nearPlane=22.4324, 
    farPlane=36.0122, width=8.17519, height=4.09344, cameraPosition=(25.2439, 
    -12.8828, 10.0611), cameraUpVector=(-0.185681, 0.776281, 0.60242), 
    cameraTarget=(3.12579, -2.85311, 4.14982), viewOffsetX=2.78027, 
    viewOffsetY=0.644761)
session.viewports['Viewport: 1'].view.setValues(nearPlane=22.2314, 
    farPlane=36.2132, width=11.0395, height=5.52765, viewOffsetX=2.25063, 
    viewOffsetY=0.794444)
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['polemount_2Jeremiah-1-1'].edges
v1 = a.instances['polemount_2Jeremiah-1-1'].vertices
a.DatumCsysByThreePoints(point2=v1[23], name='TorqueAxis', 
    coordSysType=CYLINDRICAL, 
    origin=a.instances['polemount_2Jeremiah-1-1'].InterestingPoint(edge=e1[24], 
    rule=CENTER), 
    point1=a.instances['polemount_2Jeremiah-1-1'].InterestingPoint(edge=e1[41], 
    rule=MIDDLE))
datum = mdb.models['Model-1'].rootAssembly.datums[9]
mdb.models['Model-1'].loads['TorqueLoad'].setValues(directionVector=((0.0, 0.0, 
    0.0), (1.0, 0.0, 0.0)), localCsys=datum)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.3437, 
    farPlane=35.1008, width=2.77744, height=1.23578, viewOffsetX=2.41041, 
    viewOffsetY=1.70435)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.1206, 
    farPlane=34.6233, width=2.86988, height=1.2769, cameraPosition=(26.8255, 
    -11.994, 3.38748), cameraUpVector=(-0.0684112, 0.737438, 0.671941), 
    cameraTarget=(3.58202, -2.80241, 3.33292), viewOffsetX=2.49063, 
    viewOffsetY=1.76108)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.8811, 
    farPlane=34.8627, width=4.95884, height=2.20635, viewOffsetX=2.7046, 
    viewOffsetY=1.57681)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.7408, 
    farPlane=35.8885, width=5.13734, height=2.28577, cameraPosition=(23.7378, 
    -2.06488, -15.9673), cameraUpVector=(0.151171, 0.749695, 0.644286), 
    cameraTarget=(5.03173, -1.41564, 0.598017), viewOffsetX=2.80196, 
    viewOffsetY=1.63358)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.0242, 
    farPlane=36.6051, width=11.2424, height=5.0021, viewOffsetX=4.22317, 
    viewOffsetY=1.28889)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.9183, 
    farPlane=36.711, width=11.4251, height=5.08342, viewOffsetX=4.20455, 
    viewOffsetY=1.2832)
session.viewports['Viewport: 1'].view.setValues(nearPlane=20.0892, 
    farPlane=34.6779, width=9.59608, height=4.26961, cameraPosition=(18.3389, 
    -16.6054, 15.1207), cameraUpVector=(-0.164322, 0.808088, 0.565679), 
    cameraTarget=(-0.555354, -3.38611, 5.47679), viewOffsetX=3.53144, 
    viewOffsetY=1.07777)
session.viewports['Viewport: 1'].view.setValues(nearPlane=20.666, 
    farPlane=34.1011, width=7.29957, height=3.24782, viewOffsetX=4.70454, 
    viewOffsetY=1.53418)
mdb.models['Model-1'].loads['TorqueLoad'].setValues(directionVector=((0.0, 0.0, 
    0.0), (0.0, -0.707106781186547, 0.707106781186547)))
session.viewports['Viewport: 1'].view.setValues(nearPlane=20.8119, 
    farPlane=33.9552, width=6.10571, height=2.71663, viewOffsetX=4.81563, 
    viewOffsetY=1.52619)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.6091, 
    farPlane=36.8, width=6.92634, height=3.08176, cameraPosition=(27.3263, 
    12.3734, -4.70685), cameraUpVector=(-0.561472, 0.677175, 0.475586), 
    cameraTarget=(7.85033, 0.978256, 6.04419), viewOffsetX=5.46286, 
    viewOffsetY=1.73131)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.4555, 
    farPlane=36.9536, width=6.88129, height=3.06171, viewOffsetX=5.27138, 
    viewOffsetY=0.331308)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.507, 
    farPlane=36.9021, width=6.89639, height=3.06843, cameraPosition=(27.382, 
    12.1994, -4.79037), cameraUpVector=(-0.546332, 0.673001, 0.498589), 
    cameraTarget=(7.90606, 0.80421, 5.96067), viewOffsetX=5.28295, 
    viewOffsetY=0.332035)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.8453, 
    farPlane=36.5375, width=6.99564, height=3.11259, cameraPosition=(20.6955, 
    -10.7653, 23.1944), cameraUpVector=(-0.453504, 0.810422, 0.370878), 
    cameraTarget=(0.509896, -5.48247, 9.43279), viewOffsetX=5.35898, 
    viewOffsetY=0.336814)
session.viewports['Viewport: 1'].view.setValues(nearPlane=22.5832, 
    farPlane=37.7997, width=17.8305, height=7.93339, viewOffsetX=5.26656, 
    viewOffsetY=0.786873)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=ON, loads=OFF, 
    bcs=OFF, predefinedFields=OFF, connectors=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=ON)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=OFF)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=ON)
session.viewports['Viewport: 1'].partDisplay.setValues(mesh=ON)
session.viewports['Viewport: 1'].partDisplay.meshOptions.setValues(
    meshTechnique=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
p.seedPart(size=0.05, deviationFactor=0.1, minSizeFactor=0.1)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.9423, 
    farPlane=32.4938, width=16.9558, height=7.57097, cameraPosition=(5.74121, 
    -12.1698, 24.1994), cameraUpVector=(-0.55363, 0.809502, 0.195451), 
    cameraTarget=(0.129265, -0.217876, 2.3463))
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
p.seedPart(size=0.1, deviationFactor=0.1, minSizeFactor=0.1)
elemType1 = mesh.ElemType(elemCode=C3D8I, elemLibrary=STANDARD, 
    secondOrderAccuracy=OFF, distortionControl=DEFAULT)
elemType2 = mesh.ElemType(elemCode=C3D6, elemLibrary=STANDARD)
elemType3 = mesh.ElemType(elemCode=C3D4, elemLibrary=STANDARD)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, technique=SYSTEM_ASSIGN)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
p.seedPart(size=0.5, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
c = p.cells
pickedRegions = c.getSequenceFromMask(mask=('[#1 ]', ), )
p.setMeshControls(regions=pickedRegions, elemShape=TET, technique=FREE)
elemType1 = mesh.ElemType(elemCode=C3D20R)
elemType2 = mesh.ElemType(elemCode=C3D15)
elemType3 = mesh.ElemType(elemCode=C3D10)
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1 ]', ), )
pickedRegions =(cells, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2, 
    elemType3))
p = mdb.models['Model-1'].parts['polemount_2Jeremiah-1']
p.generateMesh()
a1 = mdb.models['Model-1'].rootAssembly
a1.regenerate()
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(mesh=OFF)
session.viewports['Viewport: 1'].assemblyDisplay.meshOptions.setValues(
    meshTechnique=OFF)
mdb.Job(name='Job-1', model='Model-1', description='Torque and Face', 
    type=ANALYSIS, atTime=None, waitMinutes=0, waitHours=0, queue=None, 
    memory=90, memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True, 
    explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF, 
    modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch='', resultsFormat=ODB, multiprocessingMode=DEFAULT, numCpus=1, 
    numGPUs=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
#: The job input file "Job-1.inp" has been submitted for analysis.
#: Job Job-1: Analysis Input File Processor completed successfully.
#: Job Job-1: Abaqus/Standard completed successfully.
#: Job Job-1 completed successfully. 
o3 = session.openOdb(name='D:/School/Finite_Elements_ME486/Job-1.odb')
#: Model: D:/School/Finite_Elements_ME486/Job-1.odb
#: Number of Assemblies:         1
#: Number of Assembly instances: 0
#: Number of Part instances:     1
#: Number of Meshes:             1
#: Number of Element Sets:       5
#: Number of Node Sets:          5
#: Number of Steps:              1
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
    CONTOURS_ON_DEF, ))
session.viewports['Viewport: 1'].view.setValues(nearPlane=16.0134, 
    farPlane=32.5858, width=17.432, height=7.32432, viewOffsetX=0.000816822, 
    viewOffsetY=-0.0108279)
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(
    legendDecimalPlaces=1, legendNumberFormat=FIXED)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.3877, 
    farPlane=31.329, width=18.928, height=7.95289, cameraPosition=(24.2336, 
    0.239484, 6.99527), cameraUpVector=(-0.184113, 0.319606, -0.929491), 
    cameraTarget=(0.20924, -0.250912, 2.84012), viewOffsetX=0.000886921, 
    viewOffsetY=-0.0117571)
session.viewports['Viewport: 1'].view.setValues(nearPlane=17.2101, 
    farPlane=31.5066, width=18.7346, height=7.87164, cameraPosition=(24.234, 
    0.232393, 6.99382), cameraUpVector=(-0.166687, -0.0904025, -0.981857), 
    cameraTarget=(0.209635, -0.258003, 2.83867), viewOffsetX=0.000877859, 
    viewOffsetY=-0.011637)
session.viewports['Viewport: 1'].view.setValues(nearPlane=16.4175, 
    farPlane=31.7313, width=17.8718, height=7.5091, cameraPosition=(16.4826, 
    17.889, 2.69156), cameraUpVector=(-0.107952, -0.358515, -0.927261), 
    cameraTarget=(0.216691, -0.278914, 2.84338), viewOffsetX=0.000837428, 
    viewOffsetY=-0.011101)
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.9803, 
    farPlane=36.4026, width=5.49276, height=2.44391, viewOffsetX=6.90949, 
    viewOffsetY=0.554721)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.0221, 
    farPlane=36.3608, width=5.50233, height=2.44817, viewOffsetX=7.15019, 
    viewOffsetY=0.482681)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.3577, 
    farPlane=36.3074, width=5.57921, height=2.48238, cameraPosition=(21.9386, 
    -8.74253, 23.0736), cameraUpVector=(-0.516262, 0.77407, 0.366456), 
    cameraTarget=(1.19708, -5.40169, 9.53197), viewOffsetX=7.25009, 
    viewOffsetY=0.489425)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.3471, 
    farPlane=36.318, width=5.93275, height=2.63968, viewOffsetX=7.24572, 
    viewOffsetY=0.469539)
a = mdb.models['Model-1'].rootAssembly
del a.features['Datum csys-1']
a = mdb.models['Model-1'].rootAssembly
del a.features['TorqueAxis']
#: Warning: Cannot continue yet--complete the step or cancel the procedure.
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.3471, 
    farPlane=36.318, width=5.93276, height=2.63968, viewOffsetX=7.2393, 
    viewOffsetY=0.467786)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.0829, 
    farPlane=37.3384, width=6.35574, height=2.82788, cameraPosition=(31.9775, 
    2.80952, 8.28985), cameraUpVector=(-0.524654, 0.46045, 0.716048), 
    cameraTarget=(8.05155, -4.30018, 6.96666), viewOffsetX=7.75542, 
    viewOffsetY=0.501137)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.4568, 
    farPlane=37.9646, width=11.5169, height=5.12425, viewOffsetX=8.98575, 
    viewOffsetY=-0.0561389)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.3782, 
    farPlane=38.0432, width=11.4813, height=5.10843, cameraPosition=(31.6457, 
    3.7304, 9.34213), cameraUpVector=(-0.545933, 0.547253, 0.634406), 
    cameraTarget=(7.71971, -3.3793, 8.01894), viewOffsetX=8.958, 
    viewOffsetY=-0.0559655)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.3618, 
    farPlane=37.0597, width=3.50456, height=1.55929, viewOffsetX=6.19156, 
    viewOffsetY=0.286581)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.3891, 
    farPlane=37.0324, width=3.5082, height=1.56091, cameraPosition=(31.396, 
    4.44213, 10.0327), cameraUpVector=(-0.564528, 0.628268, 0.535339), 
    cameraTarget=(7.47002, -2.66757, 8.70956), viewOffsetX=6.19798, 
    viewOffsetY=0.286879)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.5589, 
    farPlane=36.999, width=3.53077, height=1.57096, cameraPosition=(32.5746, 
    -0.929107, 2.57318), cameraUpVector=(-0.320017, 0.558309, 0.765428), 
    cameraTarget=(8.12346, -4.78109, 6.04519), viewOffsetX=6.23786, 
    viewOffsetY=0.288725)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.6297, 
    farPlane=36.9282, width=2.77531, height=1.23483, viewOffsetX=5.27969, 
    viewOffsetY=1.7685)
a = mdb.models['Model-1'].rootAssembly
v11 = a.instances['polemount_2Jeremiah-1-1'].vertices
a.DatumPointByMidPoint(point1=v11[20], point2=v11[19])
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.3942, 
    farPlane=37.1637, width=5.1071, height=2.27232, viewOffsetX=5.06466, 
    viewOffsetY=1.84469)
a = mdb.models['Model-1'].rootAssembly
e11 = a.instances['polemount_2Jeremiah-1-1'].edges
d1 = a.datums
a.DatumCsysByThreePoints(point1=d1[10], name='TorqueAxis', 
    coordSysType=CYLINDRICAL, 
    origin=a.instances['polemount_2Jeremiah-1-1'].InterestingPoint(
    edge=e11[24], rule=CENTER), 
    point2=a.instances['polemount_2Jeremiah-1-1'].InterestingPoint(
    edge=e11[41], rule=MIDDLE))
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.1285, 
    farPlane=37.4294, width=7.32848, height=3.26068, viewOffsetX=4.94046, 
    viewOffsetY=1.84817)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(loads=ON, bcs=ON, 
    predefinedFields=ON, connectors=ON)
mdb.models['Model-1'].loads['TorqueLoad'].setValues(directionVector=((0.0, 0.0, 
    0.0), (0.0, 1.0, 0.0)))
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.5102, 
    farPlane=38.0477, width=12.4872, height=5.55595, viewOffsetX=4.98949, 
    viewOffsetY=1.85257)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.8435, 
    farPlane=38.5414, width=11.6713, height=5.19295, cameraPosition=(29.2017, 
    7.76119, -7.7473), cameraUpVector=(-0.236139, 0.552911, 0.79908), 
    cameraTarget=(9.29823, -2.15977, 3.66232), viewOffsetX=4.66351, 
    viewOffsetY=1.73153)
session.viewports['Viewport: 1'].setColor(globalTranslucency=True)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.9354, 
    farPlane=38.4497, width=11.7163, height=5.21296, cameraPosition=(28.4903, 
    7.00341, -9.64725), cameraUpVector=(-0.0508658, 0.341543, 0.938489), 
    cameraTarget=(8.5868, -2.91755, 1.76237), viewOffsetX=4.68148, 
    viewOffsetY=1.7382)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.1932, 
    farPlane=37.6971, width=12.8215, height=5.70469, cameraPosition=(32.3602, 
    -2.98686, 6.6411), cameraUpVector=(-0.368437, 0.653229, 0.661472), 
    cameraTarget=(7.44726, -4.91372, 7.26337), viewOffsetX=5.12307, 
    viewOffsetY=1.90216)
mdb.models['Model-1'].loads['TorqueLoad'].setValues(directionVector=((0.0, 0.0, 
    0.0), (0.0, 0.0, 1.0)))
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.1547, 
    farPlane=40.0132, width=12.3132, height=5.47854, cameraPosition=(25.0637, 
    -16.9584, 15.9493), cameraUpVector=(-0.866376, -0.214121, 0.45116), 
    cameraTarget=(6.23142, -6.66374, 3.13835), viewOffsetX=4.91996, 
    viewOffsetY=1.82675)
session.viewports['Viewport: 1'].view.setValues(nearPlane=24.5517, 
    farPlane=40.6163, width=18.5327, height=8.2458, viewOffsetX=3.34223, 
    viewOffsetY=2.58416)
session.viewports['Viewport: 1'].view.setValues(nearPlane=22.4789, 
    farPlane=38.6904, width=16.968, height=7.54963, cameraPosition=(24.5652, 
    16.5511, -6.45045), cameraUpVector=(-0.408718, 0.307684, 0.859232), 
    cameraTarget=(7.59141, -0.14769, 1.15193), viewOffsetX=3.06005, 
    viewOffsetY=2.36599)
session.viewports['Viewport: 1'].view.setValues(nearPlane=23.3713, 
    farPlane=37.7981, width=10.7538, height=4.78471, viewOffsetX=2.01634, 
    viewOffsetY=2.33299)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.4973, 
    farPlane=39.2189, width=11.732, height=5.21996, cameraPosition=(27.322, 
    -17.4328, 5.52177), cameraUpVector=(-0.573702, -0.0334687, 0.81838), 
    cameraTarget=(5.94747, -5.21132, 1.21833), viewOffsetX=2.19976, 
    viewOffsetY=2.54521)
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.3849, 
    farPlane=39.3312, width=11.6803, height=5.19696, cameraPosition=(27.1492, 
    -17.6883, 5.65444), cameraUpVector=(-0.541815, 0.0299003, 0.839966), 
    cameraTarget=(5.77467, -5.46682, 1.351), viewOffsetX=2.19007, 
    viewOffsetY=2.53399)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.0487, 
    farPlane=38.6674, width=6.06837, height=2.70002, viewOffsetX=3.24941, 
    viewOffsetY=2.30322)
a = mdb.models['Model-1'].rootAssembly
del a.features['TorqueAxis']
session.viewports['Viewport: 1'].view.setValues(nearPlane=25.8238, 
    farPlane=38.8923, width=8.72046, height=3.88002, viewOffsetX=3.03987, 
    viewOffsetY=2.79512)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.9905, 
    farPlane=40.106, width=9.11445, height=4.05532, cameraPosition=(29.4163, 
    7.52508, 17.6817), cameraUpVector=(-0.50899, -0.746038, 0.429367), 
    cameraTarget=(9.07402, 2.41195, 4.08754), viewOffsetX=3.17721, 
    viewOffsetY=2.9214)
session.viewports['Viewport: 1'].view.setValues(nearPlane=27.0811, 
    farPlane=39.3456, width=9.14505, height=4.06893, cameraPosition=(32.0356, 
    2.1256, 12.2243), cameraUpVector=(-0.560202, -0.605752, 0.565012), 
    cameraTarget=(9.11289, 0.413666, 2.40741), viewOffsetX=3.18788, 
    viewOffsetY=2.93121)
session.viewports['Viewport: 1'].view.setValues(nearPlane=26.7699, 
    farPlane=39.3399, width=9.03995, height=4.02217, cameraPosition=(31.6817, 
    -5.20902, 11.6076), cameraUpVector=(-0.67032, -0.412297, 0.616995), 
    cameraTarget=(8.70979, -2.01442, 2.28874), viewOffsetX=3.15124, 
    viewOffsetY=2.89752)
a = mdb.models['Model-1'].rootAssembly
e1 = a.instances['polemount_2Jeremiah-1-1'].edges
v1 = a.instances['polemount_2Jeremiah-1-1'].vertices
a.DatumCsysByThreePoints(point1=v1[23], name='TorqueCSYS', 
    coordSysType=CYLINDRICAL, 
    origin=a.instances['polemount_2Jeremiah-1-1'].InterestingPoint(edge=e1[24], 
    rule=CENTER), 
    point2=a.instances['polemount_2Jeremiah-1-1'].InterestingPoint(edge=e1[41], 
    rule=MIDDLE))
datum = mdb.models['Model-1'].rootAssembly.datums[12]
mdb.models['Model-1'].loads['TorqueLoad'].setValues(directionVector=((0.0, 0.0, 
    0.0), (0.0, 0.0, 1.0)), localCsys=datum)
