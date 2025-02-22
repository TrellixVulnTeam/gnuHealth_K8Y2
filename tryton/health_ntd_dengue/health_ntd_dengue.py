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
from datetime import datetime
from trytond.model import ModelView, ModelSingleton, ModelSQL, fields, \
    ValueMixin
from trytond.pyson import Eval, Not, Bool, PYSONEncoder
from trytond.pool import Pool
from trytond import backend
from trytond.tools.multivalue import migrate_property



__all__ = ['GnuHealthSequences', 'GnuHealthSequenceSetup', 'DengueDUSurvey']

sequences = ['dengue_du_survey_sequence']


class GnuHealthSequences(ModelSingleton, ModelSQL, ModelView):
    __name__ = 'gnuhealth.sequences'

    dengue_du_survey_sequence = fields.MultiValue(fields.Many2One(
        'ir.sequence',
        'Dengue Survey Sequence', required=True,
        domain=[('code', '=', 'gnuhealth.dengue_du_survey')]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()

        if field in sequences:
            return pool.get('gnuhealth.sequence.setup')
        return super(GnuHealthSequences, cls).multivalue_model(field)


    @classmethod
    def default_dengue_du_survey_sequence(cls):
        return cls.multivalue_model(
            'dengue_du_survey_sequence').default_dengue_du_survey_sequence()


# SEQUENCE SETUP
class GnuHealthSequenceSetup(ModelSQL, ValueMixin):
    'GNU Health Sequences Setup'
    __name__ = 'gnuhealth.sequence.setup'

    dengue_du_survey_sequence = fields.Many2One('ir.sequence', 
        'Dengue DU Survey Sequence', required=True,
        domain=[('code', '=', 'gnuhealth.dengue_du_survey')])
  
    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(GnuHealthSequenceSetup, cls).__register__(module_name)

        if not exist:
            cls._migrate_MultiValue([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.extend(sequences)
        value_names.extend(sequences)
        migrate_property(
            'gnuhealth.sequences', field_names, cls, value_names,
            fields=fields)

    @classmethod
    def default_dengue_du_survey_sequence(cls):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        return ModelData.get_id(
            'health_ntd_dengue', 'seq_gnuhealth_du_survey')
    
# END SEQUENCE SETUP , MIGRATION FROM FIELDS.MultiValue


class DengueDUSurvey(ModelSQL, ModelView):
    'Dengue DU Survey'
    __name__ = 'gnuhealth.dengue_du_survey'

    name = fields.Char('Survey Code', readonly=True)
    du = fields.Many2One('gnuhealth.du', 'DU', help="Domiciliary Unit")
    survey_date = fields.Date('Date', required=True)

    du_status = fields.Selection([
        (None, ''),
        ('initial', 'Initial'),
        ('unchanged', 'Unchanged'),
        ('better', 'Improved'),
        ('worse', 'Worsen'),
        ], 'Status',
        help="DU status compared to last visit", required=True, sort=False)

    # Surveillance traps (ovitraps)
    ovitraps = fields.Boolean(
        'Ovitraps',
        help="Check if ovitraps are in place")

    # Current issues
    aedes_larva = fields.Boolean(
        'Larvae', "Check this box if Aedes aegypti larvae were found")
    larva_in_house = fields.Boolean(
        'Domiciliary',
        help="Check this box if larvae were found inside the house")
    larva_peri = fields.Boolean(
        'Peri-Domiciliary',
        help="Check this box if larva were found in the peridomiciliary area")

    old_tyres = fields.Boolean('Tyres', help="Old vehicle tyres found")

    animal_water_container = fields.Boolean(
        'Animal Water containers',
        help="Animal water containers not scrubbed or clean")

    flower_vase = fields.Boolean(
        'Flower vase',
        help="Flower vases without scrubbing or cleaning")

    potted_plant = fields.Boolean(
        'Potted Plants',
        help="Potted Plants with saucers")

    tree_holes = fields.Boolean(
        'Tree holes',
        help="unfilled tree holes")

    rock_holes = fields.Boolean(
        'Rock holes',
        help="unfilled rock holes")

    # Chemical controls for adult mosquitoes

    du_fumigation = fields.Boolean(
        'Fumigation', help="The DU has been fumigated")
    fumigation_date = fields.Date(
        'Fumigation Date', help="Last Fumigation Date",
        states={'invisible': Not(Bool(Eval('du_fumigation')))})

    observations = fields.Text('Observations')
    next_survey_date = fields.Date('Next survey')

    @staticmethod
    def default_survey_date():
        return datetime.now()

    @classmethod
    def create(cls, vlist):
        Sequence = Pool().get('ir.sequence')
        Config = Pool().get('gnuhealth.sequences')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('name'):
                config = Config(1)
                values['name'] = Sequence.get_id(
                    config.dengue_du_survey_sequence.id)

        return super(DengueDUSurvey, cls).create(vlist)
