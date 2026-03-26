"""
Marshmallow schemas for defects endpoints.

These drive both request validation and the generated OpenAPI spec.
"""

from marshmallow import Schema, fields


class DefectSchema(Schema):
    """Full defect representation returned by the API."""

    id = fields.String(required=True, metadata={"description": "Defect identifier"})
    title = fields.String(required=True, metadata={"description": "Short defect title"})
    description = fields.String(required=False, allow_none=True, metadata={"description": "Defect description"})
    status = fields.String(required=True, metadata={"description": "Defect status"})
    severity = fields.String(required=True, metadata={"description": "Defect severity"})
    createdAt = fields.String(required=True, metadata={"description": "Creation timestamp (ISO-8601)"})
    updatedAt = fields.String(required=True, metadata={"description": "Last update timestamp (ISO-8601)"})


class DefectCreateSchema(Schema):
    """Payload accepted on create."""

    id = fields.String(required=False, allow_none=True, metadata={"description": "Optional client-provided id"})
    title = fields.String(required=True, metadata={"description": "Short defect title"})
    description = fields.String(required=False, allow_none=True, metadata={"description": "Defect description"})
    status = fields.String(required=False, allow_none=True, metadata={"description": "Defect status"})
    severity = fields.String(required=False, allow_none=True, metadata={"description": "Defect severity"})
    createdAt = fields.String(required=False, allow_none=True, metadata={"description": "Optional client timestamp"})
    updatedAt = fields.String(required=False, allow_none=True, metadata={"description": "Optional client timestamp"})


class DefectUpdateSchema(Schema):
    """Payload accepted on update (patch semantics)."""

    title = fields.String(required=False, allow_none=True, metadata={"description": "Short defect title"})
    description = fields.String(required=False, allow_none=True, metadata={"description": "Defect description"})
    status = fields.String(required=False, allow_none=True, metadata={"description": "Defect status"})
    severity = fields.String(required=False, allow_none=True, metadata={"description": "Defect severity"})
