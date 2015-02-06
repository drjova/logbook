# -*- coding: utf-8 -*-
#
# This file is part of Logbook.
# Copyright (C) 2012, 2013, 2014 CERN.
#
# Logbook is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Logbook is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Logbook; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from __future__ import absolute_import, print_function

from wtforms import validators
from invenio.base.i18n import _
from invenio.modules.deposit.types import SimpleRecordDeposition
from invenio.modules.deposit.form import WebDepositForm
from invenio.modules.deposit import fields
from invenio.modules.deposit.field_widgets import ExtendedListWidget, \
    ListItemWidget
from invenio.modules.deposit.validation_utils import list_length


def keywords_autocomplete(form, field, term, limit=50):
    return [{'value': "Keyword 1"}, {'value': "Keyword 2"}]


#
# Helpers
#
def filter_empty_helper(keys=None):
    """ Remove empty elements from a list"""
    def _inner(elem):
        if isinstance(elem, dict):
            for k, v in elem.items():
                if (keys is None or k in keys) and v:
                    return True
            return False
        else:
            return bool(elem)
    return _inner


FILE_LANGUAGES = [
    ('Text', 'Text'),
    ('MySQL', 'MySQL'),
    ('Python', 'Python'),
    ('Spanish', 'Spanish'),
    ('JavaScript', 'JavaScript'),
]


#
# Forms
#
class FileInlineForm(WebDepositForm):
    """
    Files inline form
    """
    name = fields.TextField(
        export_key='expansion',
        label=_("Name"),
        placeholder=_("Name this file..."),
        validators=[validators.Required()],
        widget_classes='form-control',
    )
    language = fields.SelectField(
        choices=FILE_LANGUAGES,
        default='Text',
        label=_("Language"),
        export_key='number',
        widget_classes='form-control',
    )
    abstract = fields.TextAreaField(
        default='',
        export_key='summary',
        icon='fa fa-pencil fa-fw',
        label=_("Description"),
        widget_classes='form-control',
    )


class GistForm(WebDepositForm):
    #
    # Fields
    #
    title = fields.TextField(
        label='',
        export_key='title.title',
        placeholder=_("Gist description..."),
        widget_classes="form-control",
    )

    gist_files = fields.DynamicFieldList(
        fields.FormField(
            FileInlineForm,
            widget=ExtendedListWidget(
                item_widget=ListItemWidget(
                    html_tag='div',
                ),
                html_tag='div',
            ),
        ),
        add_label=_('Add another file'),
        export_key='abstract',
        label='',
        min_entries=1,
        validators=[validators.Required(), list_length(
            min_num=1, element_filter=filter_empty_helper(),
        )],
        widget_classes='',
    )

    # Form configuration
    #
    _title = _('New Gist')
    _subtitle = _('Instructions: <br/>'
                  '(i) Press "Save" to save your upload for editing later, '
                  'as many times you like.<br/>'
                  '(ii) When ready, press "Submit" to finalize your upload.')

    groups = [
        ('Gist details',
            ['title', 'gist_files'],
         ),
    ]

    field_sizes = {
        'gist_files': 'col-md-10',
        'title': 'col-md-12',
    }


#
# Workflow
#
class gist(SimpleRecordDeposition):
    name = _("Gist")
    name_plural = _("Gists")
    group = _("Gists & Hists")
    draft_definitions = {
        'default': GistForm,
    }
