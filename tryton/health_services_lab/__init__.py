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
from .health_services_lab import *
from .wizard import *


def register():
    Pool.register(
    PatientLabTestRequest,
	RequestPatientLabTestStart,
        module='health_services_lab', type_='model')
    Pool.register(
        RequestPatientLabTest,
        module='health_services_lab', type_='wizard')
