import tellurium as te
import phrasedml 
import libsedml
import os
from biosimulators_utils.combine.io import CombineArchiveWriter  # type: ignore
from biomodels_qc.utils import build_combine_archive

combine_writer = CombineArchiveWriter()

def removeModelRefsFromDataGenerators(sedml):
    for dg in range(sedml.getNumDataGenerators()):
        datagen = sedml.getDataGenerator(dg)
        for v in range(datagen.getNumVariables()):
            var = datagen.getVariable(v)
            var.setModelReference("")

def globalToLocalParameter(target):
    core_id = target.split("'")[1]
    (rxn, param) = core_id.split("_")
    return "/sbml:sbml/sbml:model/sbml:listOfReactions/sbml:reaction[@id='" + rxn + "']/sbml:kineticLaw/sbml:listOfParameters/sbml:parameter[@id='" + param + "']/@value"

r = te.loads("queralt2006_final.xml")
SBML = r.getParamPromotedSBML(r.getSBML())
te.saveToFile("promoted.xml", SBML)



r = te.loads("queralt2006_final.xml")
SBML = r.getParamPromotedSBML(r.getSBML())

sedml = libsedml.readSedMLFromFile("../old_SEDML/queralt2006_final.sedml")

sedml.setVersion(4)

#Fix bugs in the generated SED-ML
# ns = sedml.getNamespaces()
# ns.add("http://www.sbml.org/sbml/level3/version1/core", "sbml")

removeModelRefsFromDataGenerators(sedml)

plot = sedml.getOutput(0)

plot.setName("Figure 7B-1")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("time(min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(50)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Number of Cells")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1.2)


curve = plot.getCurve(0)
curve.setStyle("solid_green")
curve.setName("Cdc14")
curve = plot.getCurve(1)
curve.setStyle("solid_red")
curve.setName("Cdc2")
curve = plot.getCurve(2)
curve.setStyle("solid_orange")
curve.setName("Cdh1")
curve = plot.getCurve(3)
curve.setStyle("solid_yellow")
curve.setName("Clb2")
curve = plot.getCurve(4)
curve.setStyle("solid_blue")
curve.setName("MEN")


plot = sedml.getOutput(1)

plot.setName("Figure 7B-2")

xaxis=plot.createXAxis()
xaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
xaxis.setName("time(min)")
xaxis.setGrid(False)
xaxis.setMin(0)
xaxis.setMax(50)

yaxis=plot.createYAxis()
yaxis.setType(libsedml.SEDML_AXISTYPE_LINEAR)
yaxis.setName("Number of Cells")
yaxis.setGrid(False)
yaxis.setMin(0)
yaxis.setMax(1.2)


curve = plot.getCurve(0)
curve.setStyle("solid_red")
curve.setName("Net1-P")
curve = plot.getCurve(1)
curve.setStyle("solid_blue")
curve.setName("PP2A")
curve = plot.getCurve(2)
curve.setStyle("solid_pink")
curve.setName("secunin")
curve = plot.getCurve(3)
curve.setStyle("solid_yellow")
curve.setName("separase")



style = sedml.createStyle()
line = style.createLineStyle()
line.setColor("0000ff") #blue
line.setType(libsedml.SEDML_LINETYPE_SOLID)
marker = style.createMarkerStyle()
marker.setType(libsedml.SEDML_MARKERTYPE_NONE)
style.setId("solid_blue")

style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("ff0000") #red
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_red")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("00ff00") #green
line2.setType(libsedml.SEDML_LINETYPE_SOLID)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("solid_green")


style1 = sedml.createStyle()
line1 = style1.createLineStyle()
line1.setColor("FF7F50") #orange
line1.setType(libsedml.SEDML_LINETYPE_SOLID)
marker1 = style1.createMarkerStyle()
marker1.setType(libsedml.SEDML_MARKERTYPE_NONE)
#fill = style1.createFillStyle()
#fill.setColor("#000000FF")
style1.setId("solid_orange")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("ffff00") #yellow
line2.setType(libsedml.SEDML_LINETYPE_SOLID)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("solid_yellow")

style2 = sedml.createStyle()
line2 = style2.createLineStyle()
line2.setColor("FF1493") #pink
line2.setType(libsedml.SEDML_LINETYPE_SOLID)
marker2 = style2.createMarkerStyle()
marker2.setType(libsedml.SEDML_MARKERTYPE_NONE)
style2.setId("solid_pink")





#Now fix the fact that tellurium's handling of local parameters is off:
mod1 = sedml.getModel(0)
mod1.setSource("queralt2006_final.xml")

sed = libsedml.writeSedMLToString(sedml)
te.saveToFile("queralt2006_final.sedml", sed)
te.sedml.tesedml.executeSEDML(sed, saveOutputs=True, outputDir=".")

#And clean up:
try:
    os.remove("promoted.xml")
    os.remove("manifest.xml")
except:
    pass

manifest_filename = 'manifest.xml'
sedml_filenames = ["queralt2006_final.sedml"]
archive = build_combine_archive(".", sedml_filenames)
combine_writer.run(archive, ".", "BIOMD0000000953-Fig7B.omex")
combine_writer.write_manifest(archive.contents, manifest_filename)

# print(sed)
