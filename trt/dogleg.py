#!/usr/bin/env python
## \file   trt/dogleg.py
## \author Seth R. Johnson
## \brief  Dog leg test problem

import pytrt
pytrt.print_loading_info()
################################################################################

import pytrt.mesh_twod as meshlib
from pytrt.twod_tools import Rect
from pytrt.trt_tools import ImcSolver, TrtManager, TrtSiloWriter
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

    mcplotter = McPlotter()
    writer = TrtSiloWriter( manager, ("mattemp", "opacities", "radtemp",
    "current", "eddington") )

    solver = ImcSolver( manager, imc )
    solver.add_callback( writer, 10 )
    solver.add_callback( mcplotter, 1 )
    solver.solve()

#******************************************************************************#
if __name__ == '__main__':
    imc_solver()

