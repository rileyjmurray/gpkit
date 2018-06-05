"Implements the relaxed constants and/or constraints SP solution algorithm"

from gpkit import Model
from gpkit.constraints.relax import ConstantsRelaxed, ConstraintsRelaxed, ConstraintsRelaxedEqually

class RelaxedConstantsModel(Model):
    def setup(self, model, include_only=None, exclude_only=None):
        """
        Method to precondition an SP so it solves with a relaxed constants algorithm

        ARGUMENTS
        ---------
        model: the model to solve with relaxed constants

        RETURNS
        -------
        feas: the input model but with relaxed constants and a new objective
        """
        self.include_only = None
        self.exclude_only = None
        if include_only:
            self.include_only = include_only
        if exclude_only:
            self.exclude_only = exclude_only
        if model.substitutions:
            constsrelaxed = ConstantsRelaxed(model, self.include_only, self.exclude_only)
            feas = Model(constsrelaxed.relaxvars.prod()**20 * model.cost,
                         constsrelaxed)
        else:
            feas = Model(model.cost, model)
        return feas

# class RelaxedConstraintsModel(Model):
#     def setup(self, model):
#         """
#         Method to precondition an SP so it solves with a relaxed constraints algorithm
#
#         ARGUMENTS
#         ---------
#         model: the model to solve with relaxed constraints
#
#         RETURNS
#         -------
#         feas: the input model but with relaxed constraints and a new objective
#         """
#         constraintsrelaxed = ConstraintsRelaxed(model)
#         feas = Model(constraintsrelaxed.relaxvars.prod()**20 * model.cost,
#                          constraintsrelaxed)
#         return feas

def post_process(sol):
    """
    Model to print relevant info for a solved model with relaxed constants

    ARGUMENTS
    --------
    sol: the solution to the solved model
    """
    warning = "WARNING: The final GP had relaxation values greater than 1"
    print "Checking for relaxed constants..."
    for i in range(len(sol.program.gps)):
        varkeys = [k for k in sol.program.gps[i].varlocs
                   if "Relax" in k.models
                   and sol.program.gps[i].result(k) >= 1.00001]
        if varkeys:
            print "GP iteration %s has relaxed constants" % i
            print sol.program.gps[i].result.table(varkeys)
            if i == len(sol.program.gps) - 1:
                print warning
