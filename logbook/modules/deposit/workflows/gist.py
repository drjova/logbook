# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2012, 2013, 2014 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from __future__ import absolute_import, print_function

from wtforms import validators
from werkzeug.local import LocalProxy
from invenio.base.i18n import _, language_list_long
from datetime import date
from invenio.modules.deposit.types import SimpleRecordDeposition
from invenio.modules.deposit.form import WebDepositForm
from invenio.modules.deposit import fields
from invenio.modules.deposit.filter_utils import strip_string, sanitize_html, \
    strip_prefixes
from invenio.modules.deposit.field_widgets import date_widget, \
    plupload_widget, ExtendedListWidget, CKEditorWidget, \
    ColumnInput, ItemWidget
from invenio.modules.deposit.validation_utils import required_if, \
    list_length, doi_syntax_validator


def keywords_autocomplete(form, field, term, limit=50):
    return [{'value': "Keyword 1"}, {'value': "Keyword 2"}]


def missing_doi_warning(dummy_form, field, submit=False, fields=None):
    """
    Field processor, checking for existence of a DOI, and otherwise
    asking people to provide it.
    """
    if not field.errors and not field.data:
        field.add_message("Please provide a DOI if possible.", state="warning")
        raise StopIteration()


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


#
# Forms
#
class AuthorInlineForm(WebDepositForm):
    """
    Author inline form
    """
    name = fields.TextField(
        placeholder=_("Family name, First name"),
        widget_classes='form-control',
        #autocomplete=map_result(
        #    dummy_autocomplete,
        #    authorform_mapper
        #),
        widget=ColumnInput(class_="col-xs-6"),
        validators=[
            required_if(
                'affiliation',
                [lambda x: bool(x.strip()), ],  # non-empty
                message=_("Creator name is required if you specify affiliation.")
            ),
        ],
    )
    affiliation = fields.TextField(
        placeholder=_("Affiliation"),
        widget_classes='form-control',
        widget=ColumnInput(class_="col-xs-4 col-pad-0"),
    )


class GistForm(WebDepositForm):
    #
    # Fields
    #

    title = fields.TextField(
        label=_('Gist description'),
        export_key='description',
        widget_classes="form-control",
        validators=[validators.Required()],
    )

    keywords = fields.DynamicFieldList(
        fields.TextField(
            widget_classes='form-control',
            widget=ColumnInput(class_="col-xs-10"),
        ),
        label='Keywords',
        add_label='Add another keyword',
        icon='fa fa-tags fa-fw',
        widget_classes='',
        min_entries=1,
    )

    #
    # Form configuration
    #
    _title = _('New gist')

#
# Workflow
#
class gist(SimpleRecordDeposition):
    name = _("Gist")
    name_plural = _("Gists")
    group = _("Gists & Recipies")
    draft_definitions = {
        'default': GistForm,
    }

    @classmethod
    def process_sip_metadata(cls, deposition, metadata):
        # Map keywords to match jsonalchemy configuration
        metadata['keywords'] = map(
            lambda x: {'term': x},
            metadata['keywords']
        )
