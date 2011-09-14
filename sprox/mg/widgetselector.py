"""
widgetselecter Module

this contains the class which allows the ViewConfig to select the appropriate widget for the given field

Classes:
Name                               Description
MingWidgetSelecter                Aid for the selection of a widget to correspond to a Ming Document field

Exceptions:
None

Functions:
None


Copyright (c) 2009 Christopher Perkins
Original Version by Christopher Perkins 2009
Released under MIT license.

Mongo Contributions by Jorge Vargas
"""

from sprox.widgetselector import WidgetSelector
from sprox.widgets import *
from tw.forms import TextField, FileField, Label, TextArea, PasswordField

from ming import schema as S
from ming.orm.property import RelationProperty, ManyToOneJoin, OneToManyJoin

class MingWidgetSelector(WidgetSelector):

    default_multiple_select_field_widget_type = PropertyMultipleSelectField
    default_single_select_field_widget_type = PropertySingleSelectField

    default_widgets = {
    S.Bool: SproxCheckBox,
    S.Int: TextField,
    S.Float: TextField,
    S.String: TextField,
    S.DateTime: SproxCalendarDateTimePicker,
    S.Binary: FileField,
    S.Value: Label,
    S.ObjectId: TextField
    }
    def select(self,field):

        if isinstance(field, RelationProperty):
            join = field.join
            if isinstance(join, ManyToOneJoin):
                return self.default_single_select_field_widget_type
            if isinstance(join, OneToManyJoin):
                return self.default_multiple_select_field_widget_type
            raise NotImplementedError("Unknown join type %r" % join)	# pragma: no cover
        
        f = getattr(field, 'field', None)
        if f is not None:
            schemaitem = S.SchemaItem.make(field.field.type)
        else:
            return TextField

        if isinstance(schemaitem, S.OneOf):
            return self.default_single_select_field_widget_type

        #i don't think this works in the latest ming
        sprox_meta = getattr(field, "sprox_meta", {})
        if sprox_meta.get("narrative"):
            return TextArea
        if field.name == "password":
            return PasswordField
        sprox_meta = getattr(field, 'sprox_meta', None)
        if sprox_meta and 'password' in sprox_meta:
            return PasswordField
        
        return self.default_widgets.get(schemaitem.__class__, TextField)
