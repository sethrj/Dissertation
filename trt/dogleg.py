#!/usr/bin/env python
## \file   trt/dogleg.py
## \author Seth R. Johnson
## \brief  Dog leg test problem

import pytrt
pytrt.print_loading_info()
################################################################################

import pytrt.mesh_twod as meshlib
from pytrt.twod_tools import Rect
from pytrt.trt_tools import ImcSolver, TrtManager
from pytrt.td_tools import EventManager
from pytrt.mc_tools import McPlotter

import pytrt.trt_imc_gray_flatland as imc
import pytrt.mesh_twod as meshlib
import pytrt.physics_gray as physics

################################################################################
class TrtDoglegManager(TrtManager):
    def __init__(self):
        self.name = "trtdogleg"

        self.thick_matl = physics.Material(
                physics.SpecificHeatModelConstant( 1.0 ),
                physics.OpacityModelInvCubic(1.0)
                )
        self.src_matl = physics.Material(
                physics.SpecificHeatModelConstant( 1.0 ),
                physics.OpacityModelConstant(0.5)
                )
        self.thin_matl = physics.Material(
                physics.SpecificHeatModelConstant( 0.5 ),
                physics.OpacityModelInvCubic(0.01)
                )

        self.maxtime = 100.0
        self.deltat = 0.05
        self.numparticles = 1000000
        self.conservation_verbosity = physics.EnergyAccountant.WARNONLY

        TrtManager.__init__(self, meshlib, flatland=True)

    def create_mesh(self):
        widths = (
                 [0.2] * 12 + [0.1] * 6 +
                 [0.1] * 6 + [0.2] * 9 + [0.1] * 6 + #middle
                 [0.1] * 6 + [0.2] * 9 + [0.1] * 6 + #middle
                 [0.1] * 6 + [0.2] * 12 #middle
                 )
        heights = (
                 [0.2] * 15 + # source
                 [0.2] * 15 + # duct (3 cm)
                 #[0.2] * 12 + [0.1] * 4 +  [0.05] * 4 + #duct (3 cm)
                 [0.2] * 12 + [0.1] * 6 + #duct (3 cm)
                 [0.1] * 5 + [0.2] * 10 + [0.1] * 5 + #middle
                 [0.1] * 6 + [0.2] * 12 + #top (3 cm)
                 [0.2] * 15 # duct
                 )

        self.mesh = meshlib.Mesh( 0.0, 0.0,
                widths, heights )

    def initialize_data(self):
        self.material.assign( self.thick_matl)
        self.source.assign( 0.0 )

        self.ic_material = meshlib.CellFieldFloat(self.mesh, 0.1)
        self.ic_radiation = self.ic_material

        # source rectangle
        src_rect = Rect( (0.0, 0.0), (3.0, 3.0) )

        # rectangles that comprise dog leg
        dogleg = (
                Rect( (0.0, 3.0),  (3.0, 12.0) ),
                Rect( (3.0, 9.0),  (9.0, 12.0) ),
                Rect( (6.0, 12.0), (9.0, 18.0) ),
                )
        for c in self.mesh.cells():
            center = tuple( c.getCenter() )
            if src_rect.is_point_inside( center ):
                self.source[ c ] = 1.0
                self.material[ c ] = self.src_matl
                self.ic_material[ c ] = 0.2
                continue

            for r in dogleg:
                if r.is_point_inside( center ):
                    self.material[ c ] = self.thin_matl
                    break

    def set_bcs(self, p, module):
        p.setRightBoundaryCondition(   module.VacuumBcGenerator )
        p.setBottomBoundaryCondition(  module.VacuumBcGenerator )
        p.setLeftBoundaryCondition(    module.ReflectingBcGenerator )
        p.setTopBoundaryCondition(     module.ReflectingBcGenerator )

    #------------------------------------------------------------#
    # SOLVER
    def timestep(self, time_index, time):
        "Return delta t given some time index and time"
        return self.deltat

################################################################################
def imc_solver():
    "Run the simulation"
    manager = TrtDoglegManager()

    mattemp = [ manager.ic_material ]
    mcplotter = McPlotter( ("census",) )

    solver = ImcSolver( manager, imc )

    sigma_a = meshlib.CellFieldFloat( manager.mesh )
    sigma_es = meshlib.CellFieldFloat( manager.mesh )

    radtemp = meshlib.CellFieldFloat( manager.mesh )
    current = meshlib.CellFieldVector( manager.mesh )
    eddington = meshlib.CellFieldTensor( manager.mesh )

    writer = meshlib.SiloWriter( "%s%04d.silo" % (manager.name, 0) )
    writer.write( manager.mesh, "mesh" )
    writer.write( manager.ic_material, "mattemp" )
    writer.write( manager.ic_radiation, "radtemp" )
    writer.write( current, "current" )
    writer.write( eddington, "eddington" )

    solver.get_opacities( sigma_a, sigma_es )
    writer.write( sigma_a, "sigma")
    writer.write( sigma_es, "sigma_es")
    writer.suspend()

    for (time, solution) in solver:
        ti = solver.time_index

        mcplotter.update( time, solution )

        #if ti in (1,2,5,10,20,50,100,150,200,250,300,350,400):
        if ti % 10 == 0:
            writer.newTimeStep("%s%04d.silo" % (manager.name, ti), ti, time)
            writer.write( manager.mesh, "mesh" )
            writer.write( solution.getTemperature(), "mattemp" )

            solution.getMoments( radtemp, current, eddington )
            writer.write( radtemp, "radtemp" )
            writer.write( current, "current" )
            writer.write( eddington, "eddington" )

            solver.get_opacities( sigma_a, sigma_es )
            writer.write( sigma_a, "sigma")
            writer.write( sigma_es, "sigma_es")

            writer.suspend()

#******************************************************************************#
if __name__ == '__main__':
    imc_solver()

