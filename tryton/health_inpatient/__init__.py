# -*- coding: utf-8 -*-
##############################################################################
#
#    GNU Health: The Free Health and Hospital Information System
#    Copyright (C) 2008-2018 Luis Falcon <lfalcon@gnusolidario.org>
#    Copyright (C) 2011-2018 GNU Solidario <health@gnusolidario.org>
#
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from trytond.pool import Pool
from .health_inpatient import *
from .wizard import *


def register():
    Pool.register(
        GnuHealthSequences,
        GnuHealthSequenceSetup,
        DietTherapeutic,
        InpatientRegistration,
        BedTransfer,
        Appointment,
        PatientEvaluation,
        ECG,
        PatientData,
        InpatientMedication,
        InpatientMedicationAdminTimes,
        InpatientMedicationLog,
        InpatientDiet,
        CreateBedTransferInit,
        InpatientMeal,
        InpatientMealOrder,
        InpatientMealOrderItem,
        module='health_inpatient', type_='model')
    
    Pool.register(
        CreateBedTransfer,
        CreateInpatientEvaluation,
        module='health_inpatient', type_='wizard')

